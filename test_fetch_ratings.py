from datetime import date

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import scoring.fetch_ratings as fetch_ratings
from db.models import Base, MatchRating, Player


def test_get_player_match_ratings_filters_by_week(monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)
    monkeypatch.setattr(fetch_ratings, "SessionLocal", Session)

    db = Session()
    player = Player(name="Test Player", position="Striker", club="Test FC")
    db.add(player)
    db.commit()
    db.refresh(player)
    player_id = player.id

    db.add_all(
        [
            MatchRating(
                player_id=player.id,
                source="sofascore",
                rating=8.0,
                match_date=date(2025, 1, 7),  # ISO week 2
                competition="League",
            ),
            MatchRating(
                player_id=player.id,
                source="fotmob",
                rating=7.5,
                match_date=date(2025, 1, 18),  # ISO week 3
                competition="League",
            ),
        ]
    )
    db.commit()
    db.close()

    week_two_ratings = fetch_ratings.get_player_match_ratings(player_id, 2)

    assert len(week_two_ratings) == 1
    assert week_two_ratings[0]["source"] == "sofascore"
