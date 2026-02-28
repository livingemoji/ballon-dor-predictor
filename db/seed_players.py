from db.database import SessionLocal
from db.models import Player


DEFAULT_PLAYERS = [
    {"name": "Kylian Mbappe", "position": "Striker", "club": "Real Madrid"},
    {"name": "Erling Haaland", "position": "Striker", "club": "Manchester City"},
    {"name": "Jude Bellingham", "position": "Midfielder", "club": "Real Madrid"},
    {"name": "Vinicius Junior", "position": "Winger", "club": "Real Madrid"},
    {"name": "Rodri", "position": "Midfielder", "club": "Manchester City"},
]

VALID_POSITIONS = {"Striker", "Winger", "Midfielder", "Defender", "Goalkeeper"}


def _normalize_position(position: str | None) -> str:
    if position in VALID_POSITIONS:
        return position
    return "Striker"


def seed_players() -> tuple[int, int]:
    created = 0
    updated = 0
    db = SessionLocal()

    try:
        for payload in DEFAULT_PLAYERS:
            name = payload["name"].strip()
            position = _normalize_position(payload.get("position"))
            club = payload.get("club")
            existing = db.query(Player).filter(Player.name == name).one_or_none()
            if existing:
                existing.position = position
                existing.club = club
                updated += 1
                continue

            db.add(Player(name=name, position=position, club=club))
            created += 1

        db.commit()
        return created, updated
    finally:
        db.close()


if __name__ == "__main__":
    created_count, updated_count = seed_players()
    print(f"Seed complete. created={created_count}, updated={updated_count}")
