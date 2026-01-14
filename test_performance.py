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