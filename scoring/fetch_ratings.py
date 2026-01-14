from db.database import SessionLocal
from db.models import MatchRating


def get_player_match_ratings(player_id: int, week: int):
    """
    NOTE:
    For now, we assume 'week' maps to match_date externally.
    This will be improved later.
    """

    db = SessionLocal()

    ratings = (
        db.query(MatchRating)
        .filter(MatchRating.player_id == player_id)
        .all()
    )

    db.close()

    return [
        {
            "source": r.source,
            "rating": r.rating,
            "competition": r.competition,
        }
        for r in ratings
    ]