from typing import Dict, List

from fastapi import APIRouter
from pydantic import BaseModel
from sqlalchemy import func

from db.database import SessionLocal
from db.models import Player, Sentiment, WeeklyScore
from engine.weekly_engine import WeeklyScoringEngine
from analysis.fallback_pipeline import get_crucial_actions_for_player
from scoring.aggregation import aggregate_performance
from scoring.fetch_ratings import get_player_match_ratings


router = APIRouter()
VALID_POSITIONS = {"Striker", "Winger", "Midfielder", "Defender", "Goalkeeper"}


class WeeklyRunRequest(BaseModel):
    week: int
    include_crucial_actions: bool = False


@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


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


@router.post("/run-weekly")
def run_weekly(payload: WeeklyRunRequest) -> Dict:
    engine = WeeklyScoringEngine()
    db = SessionLocal()
    output = []

    try:
        players = db.query(Player).all()

        for player in players:
            ratings = get_player_match_ratings(player.id, payload.week)
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
                }
            )

        db.commit()
        return {"week": payload.week, "updated_players": len(output), "scores": output}
    finally:
        db.close()
