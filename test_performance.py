from scoring.aggregation import aggregate_performance


def test_aggregate_performance_with_competition_weights():
    score = aggregate_performance(
        [
            {"source": "sofascore", "rating": 8.7, "competition": "Champions League"},
            {"source": "fotmob", "rating": 8.2, "competition": "League"},
        ]
    )

    assert score == 0.661
