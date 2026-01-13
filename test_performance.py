from scoring.aggregation import aggregate_performance

mock_ratings = [
    {
        "source": "sofascore",
        "rating": 8.7,
        "competition": "Champions League"
    },
    {
        "source": "fotmob",
        "rating": 8.2,
        "competition": "League"
    }
]

score = aggregate_performance(mock_ratings)

print("Aggregated performance score:", round(score, 3))
assert 0.0 <= score <= 1.0, "Score should be normalized between 0 and 1"