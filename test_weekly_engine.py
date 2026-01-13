from engine.weekly_engine import WeeklyScoringEngine

engine = WeeklyScoringEngine()

mock_performances = [
    {"source": "sofascore", "rating": 8.6, "competition": "Champions League"},
    {"source": "fotmob", "rating": 8.1, "competition": "League"}
]

mock_sentiment = 0.55  # positive online sentiment

score = engine.compute_week_score(
    performances=mock_performances,
    sentiment_score=mock_sentiment
)

print("Weekly player score:", score)
