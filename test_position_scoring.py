from engine.weekly_engine import WeeklyScoringEngine


def test_position_scoring_profile_changes_output():
    engine = WeeklyScoringEngine()

    defender_score = engine.compute_week_score(
        performances=[{"source": "sofascore", "rating": 7.6, "competition": "League"}],
        sentiment_score=0.2,
        position="Defender",
        stats={"goals": 1, "assists": 0, "defensive_actions": 6},
        crucial_actions=2,
    )

    striker_score = engine.compute_week_score(
        performances=[{"source": "fotmob", "rating": 8.2, "competition": "League"}],
        sentiment_score=0.4,
        position="Striker",
        stats={"goals": 1, "assists": 0, "defensive_actions": 0},
        crucial_actions=0,
    )

    assert defender_score > striker_score
