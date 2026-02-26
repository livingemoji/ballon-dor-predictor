from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base, Player


def test_player_insert_roundtrip():
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = Session()
    player = Player(
        name="Erling Haaland",
        position="Striker",
        club="Manchester City",
    )
    db.add(player)
    db.commit()
    db.refresh(player)

    assert player.id is not None
    assert player.name == "Erling Haaland"
    db.close()
