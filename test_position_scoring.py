from engine.weekly_engine import WeeklyScoringEngine

engine = WeeklyScoringEngine()

# Defender with a goal + crucial clearance
defender_score = engine.compute_week_score(
    performances=[{"source": "sofascore", "rating": 7.6, "competition": "League"}],
    sentiment_score=0.2,
    position="Defender",
    stats={
        "goals": 1,
        "assists": 0,
        "defensive_actions": 6
    },
    crucial_actions=2
)

# Striker with a goal
striker_score = engine.compute_week_score(
    performances=[{"source": "fotmob", "rating": 8.2, "competition": "League"}],
    sentiment_score=0.4,
    position="Striker",
    stats={
        "goals": 1,
        "assists": 0,
        "defensive_actions": 0
    },
    crucial_actions=0
)

print("Defender score:", defender_score)
print("Striker score:", striker_score)
