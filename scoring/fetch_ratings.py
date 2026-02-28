from db.database import SessionLocal
from db.models import MatchRating


def get_player_match_ratings(player_id: int, week: int, db_session=None):
    """
    NOTE:
    For now, we assume 'week' maps to match_date externally.
    This will be improved later.
    """

    db = db_session or SessionLocal()
    should_close = db_session is None
    try:
        ratings = (
            db.query(MatchRating)
            .filter(MatchRating.player_id == player_id)
            .all()
        )
    finally:
        if should_close:
            db.close()

    return [
        {
            "source": r.source,
            "rating": r.rating,
            "competition": r.competition,
        }
        for r in ratings
        if r.match_date and r.match_date.isocalendar().week == week
    ]
