from datetime import date, datetime
from typing import Dict, List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import func

from data_sources.performances import fetch_player_performance
from data_sources.social_sentiment import fetch_social_posts
from db.database import SessionLocal
from db.models import JobRun, MatchRating, Player, Sentiment, WeeklyScore
from engine.weekly_engine import WeeklyScoringEngine
from analysis.fallback_pipeline import get_crucial_actions_for_player
from scoring.aggregation import aggregate_performance
from scoring.fetch_ratings import get_player_match_ratings
from sentiment.sentiment_pipeline import SentimentPipeline


router = APIRouter()
VALID_POSITIONS = {"Striker", "Winger", "Midfielder", "Defender", "Goalkeeper"}
DEFAULT_PLAYERS = [
    {"name": "Kylian Mbappe", "position": "Striker", "club": "Real Madrid"},
    {"name": "Erling Haaland", "position": "Striker", "club": "Manchester City"},
    {"name": "Jude Bellingham", "position": "Midfielder", "club": "Real Madrid"},
    {"name": "Vinicius Junior", "position": "Winger", "club": "Real Madrid"},
    {"name": "Rodri", "position": "Midfielder", "club": "Manchester City"},
]


class SeedPlayer(BaseModel):
    name: str = Field(min_length=1)
    position: str = Field(default="Striker")
    club: str | None = None


class SeedPlayersRequest(BaseModel):
    players: List[SeedPlayer] = Field(default_factory=list)


def _normalize_position(position: str | None) -> str:
    if position in VALID_POSITIONS:
        return position
    return "Striker"


class WeeklyRunRequest(BaseModel):
    week: int = Field(ge=1, le=53)
    include_crucial_actions: bool = False


def _week_start_date(week: int, year: int) -> date:
    try:
        return date.fromisocalendar(year, week, 1)
    except ValueError:
        return date.fromisocalendar(year, 52, 1)


def _ingest_weekly_ratings(db, player: Player, week: int, year: int) -> int:
    added = 0
    match_date = _week_start_date(week, year)
    source_ratings = fetch_player_performance(player.name)
    for item in source_ratings:
        source = item.get("source")
        rating = item.get("rating")
        competition = item.get("competition", "League")
        if source is None or rating is None:
            continue

        exists = (
            db.query(MatchRating)
            .filter(
                MatchRating.player_id == player.id,
                MatchRating.source == source,
                MatchRating.match_date == match_date,
                MatchRating.competition == competition,
            )
            .one_or_none()
        )
        if exists:
            exists.rating = float(rating)
            continue

        db.add(
            MatchRating(
                player_id=player.id,
                source=source,
                rating=float(rating),
                minutes_played=None,
                match_date=match_date,
                competition=competition,
            )
        )
        added += 1
    return added


def _ingest_weekly_sentiments(
    db,
    player: Player,
    week: int,
    sentiment_pipeline: SentimentPipeline,
) -> int:
    posts = fetch_social_posts(player.name)
    structured_posts = [
        {
            "player_id": player.id,
            "text": text,
            "source": "social",
            "week": week,
        }
        for text in posts
        if text
    ]
    sentiment_results = sentiment_pipeline.process_posts(structured_posts)
    added = 0
    for item in sentiment_results:
        exists = (
            db.query(Sentiment)
            .filter(
                Sentiment.player_id == player.id,
                Sentiment.week == week,
                Sentiment.source == item["source"],
                Sentiment.text == item["text"],
            )
            .one_or_none()
        )
        if exists:
            exists.vader_score = float(item["vader_score"])
            exists.llm_score = item["llm_score"]
            continue

        db.add(
            Sentiment(
                player_id=player.id,
                text=item["text"],
                source=item["source"],
                week=week,
                vader_score=float(item["vader_score"]),
                llm_score=item["llm_score"],
            )
        )
        added += 1
    return added


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@router.post("/seed-players")
def seed_players(payload: SeedPlayersRequest) -> Dict:
    db = SessionLocal()
    created = 0
    updated = 0

    try:
        candidates = payload.players or [SeedPlayer(**p) for p in DEFAULT_PLAYERS]
        for candidate in candidates:
            existing = (
                db.query(Player)
                .filter(Player.name == candidate.name.strip())
                .one_or_none()
            )
            normalized_position = _normalize_position(candidate.position)
            if existing:
                existing.position = normalized_position
                existing.club = candidate.club
                updated += 1
                continue

            db.add(
                Player(
                    name=candidate.name.strip(),
                    position=normalized_position,
                    club=candidate.club,
                )
            )
            created += 1

        db.commit()
        return {
            "created": created,
            "updated": updated,
            "total_submitted": len(candidates),
        }
    finally:
        db.close()


@router.get("/leaderboard")
def leaderboard(limit: int = 20) -> List[Dict]:
    db = SessionLocal()
    try:
        rows = (
            db.query(
                Player.name.label("player_name"),
                func.sum(WeeklyScore.final_score).label("season_total"),
                func.max(WeeklyScore.week).label("latest_week"),
            )
            .join(WeeklyScore, WeeklyScore.player_id == Player.id)
            .group_by(Player.id, Player.name)
            .order_by(func.sum(WeeklyScore.final_score).desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()

    return [
        {
            "player_name": row.player_name,
            "season_total": round(float(row.season_total or 0.0), 4),
            "latest_week": row.latest_week,
        }
        for row in rows
    ]


@router.get("/job-runs")
def list_job_runs(limit: int = 20) -> List[Dict]:
    db = SessionLocal()
    try:
        runs = (
            db.query(JobRun)
            .order_by(JobRun.started_at.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()

    return [
        {
            "id": run.id,
            "week": run.week,
            "status": run.status,
            "started_at": run.started_at.isoformat() if run.started_at else None,
            "finished_at": run.finished_at.isoformat() if run.finished_at else None,
            "updated_players": run.updated_players,
            "ingested_ratings_count": run.ingested_ratings_count,
            "ingested_sentiments_count": run.ingested_sentiments_count,
            "error_message": run.error_message,
        }
        for run in runs
    ]


@router.get("/weeks/{week}/snapshot")
def week_snapshot(week: int) -> Dict:
    db = SessionLocal()
    try:
        rows = (
            db.query(
                WeeklyScore.player_id,
                Player.name.label("player_name"),
                WeeklyScore.performance_score,
                WeeklyScore.sentiment_score,
                WeeklyScore.final_score,
            )
            .join(Player, Player.id == WeeklyScore.player_id)
            .filter(WeeklyScore.week == week)
            .order_by(WeeklyScore.final_score.desc())
            .all()
        )
    finally:
        db.close()

    players = [
        {
            "rank": idx + 1,
            "player_id": row.player_id,
            "player_name": row.player_name,
            "performance_score": round(float(row.performance_score), 4),
            "sentiment_score": round(float(row.sentiment_score), 4),
            "final_score": round(float(row.final_score), 4),
        }
        for idx, row in enumerate(rows)
    ]
    return {"week": week, "count": len(players), "players": players}


@router.get("/players/{player_id}/history")
def player_history(player_id: int, limit: int = 52) -> Dict:
    db = SessionLocal()
    try:
        player = db.query(Player).filter(Player.id == player_id).one_or_none()
        if player is None:
            raise HTTPException(status_code=404, detail="Player not found")

        history_rows = (
            db.query(WeeklyScore)
            .filter(WeeklyScore.player_id == player_id)
            .order_by(WeeklyScore.week.desc())
            .limit(limit)
            .all()
        )
    finally:
        db.close()

    history = [
        {
            "week": row.week,
            "performance_score": round(float(row.performance_score), 4),
            "sentiment_score": round(float(row.sentiment_score), 4),
            "final_score": round(float(row.final_score), 4),
        }
        for row in reversed(history_rows)
    ]
    return {
        "player_id": player.id,
        "player_name": player.name,
        "position": player.position,
        "club": player.club,
        "history": history,
    }


@router.post("/run-weekly")
def run_weekly(payload: WeeklyRunRequest) -> Dict:
    engine = WeeklyScoringEngine()
    sentiment_pipeline = SentimentPipeline()
    db = SessionLocal()
    output = []
    total_ingested_ratings = 0
    total_ingested_sentiments = 0
    now = datetime.utcnow()
    existing_running_job = (
        db.query(JobRun)
        .filter(JobRun.week == payload.week, JobRun.status == "running")
        .one_or_none()
    )
    if existing_running_job is not None:
        db.close()
        raise HTTPException(
            status_code=409,
            detail=f"Week {payload.week} already has a running job (id={existing_running_job.id})",
        )

    job_run = JobRun(
        week=payload.week,
        status="running",
        started_at=now,
        updated_players=0,
        ingested_ratings_count=0,
        ingested_sentiments_count=0,
    )
    db.add(job_run)
    db.commit()
    db.refresh(job_run)

    try:
        players = db.query(Player).all()
        season_year = date.today().year

        for player in players:
            ingested_ratings = _ingest_weekly_ratings(db, player, payload.week, season_year)
            ingested_sentiments = _ingest_weekly_sentiments(
                db, player, payload.week, sentiment_pipeline
            )
            total_ingested_ratings += ingested_ratings
            total_ingested_sentiments += ingested_sentiments
            db.flush()

            ratings = get_player_match_ratings(player.id, payload.week, db_session=db)
            if not ratings:
                continue

            sentiment_avg = (
                db.query(func.avg(func.coalesce(Sentiment.llm_score, Sentiment.vader_score)))
                .filter(Sentiment.player_id == player.id, Sentiment.week == payload.week)
                .scalar()
            )
            sentiment_score = float(sentiment_avg or 0.0)
            stats = {"goals": 0, "assists": 0, "defensive_actions": 0}
            crucial_actions = 0
            if payload.include_crucial_actions:
                try:
                    crucial_actions = get_crucial_actions_for_player(player.name)
                except Exception:
                    crucial_actions = 0

            position = player.position if player.position in VALID_POSITIONS else "Striker"
            final_score = engine.compute_week_score(
                performances=ratings,
                sentiment_score=sentiment_score,
                position=position,
                stats=stats,
                crucial_actions=crucial_actions,
            )

            performance_score = aggregate_performance(ratings)

            existing = (
                db.query(WeeklyScore)
                .filter(WeeklyScore.player_id == player.id, WeeklyScore.week == payload.week)
                .one_or_none()
            )
            if existing:
                existing.performance_score = performance_score
                existing.sentiment_score = sentiment_score
                existing.final_score = final_score
            else:
                db.add(
                    WeeklyScore(
                        player_id=player.id,
                        week=payload.week,
                        performance_score=performance_score,
                        sentiment_score=sentiment_score,
                        final_score=final_score,
                    )
                )

            output.append(
                {
                    "player_id": player.id,
                    "player_name": player.name,
                    "week": payload.week,
                    "score": final_score,
                    "ingested_ratings": ingested_ratings,
                    "ingested_sentiments": ingested_sentiments,
                }
            )

        job_run.status = "completed"
        job_run.finished_at = datetime.utcnow()
        job_run.updated_players = len(output)
        job_run.ingested_ratings_count = total_ingested_ratings
        job_run.ingested_sentiments_count = total_ingested_sentiments
        db.commit()
        return {
            "job_run_id": job_run.id,
            "week": payload.week,
            "status": job_run.status,
            "updated_players": len(output),
            "ingested_ratings_count": total_ingested_ratings,
            "ingested_sentiments_count": total_ingested_sentiments,
            "scores": output,
        }
    except Exception as exc:
        db.rollback()
        job_run.status = "failed"
        job_run.finished_at = datetime.utcnow()
        job_run.error_message = str(exc)[:500]
        db.commit()
        raise
    finally:
        db.close()
