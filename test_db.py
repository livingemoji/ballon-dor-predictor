from db.database import SessionLocal
from db.models import Player

db = SessionLocal()

player = Player(
    name="Erling Haaland",
    position="Forward",
    club="Manchester City"
)

db.add(player)
db.commit()
db.refresh(player)

print(player.id, player.name)

db.close()
