import pytest

from engine.weekly_engine import WeeklyScoringEngine


def test_compute_week_score_with_all_required_inputs():
    engine = WeeklyScoringEngine()

    score = engine.compute_week_score(
        performances=[
            {"source": "sofascore", "rating": 8.6, "competition": "Champions League"},
            {"source": "fotmob", "rating": 8.1, "competition": "League"},
        ],
        sentiment_score=0.55,
        position="Striker",
        stats={"goals": 1, "assists": 1, "defensive_actions": 0},
        crucial_actions=1,
    )

    assert score == pytest.approx(1.4036, rel=1e-4)
