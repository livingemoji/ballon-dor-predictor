from sentiment.sentiment_pipeline import SentimentPipeline


def test_sentiment_pipeline_produces_scores_and_keeps_metadata():
    pipeline = SentimentPipeline()
    results = pipeline.process_posts(
        [
            {
                "player_id": 1,
                "text": "I absolutely love this amazing player. Brilliant and excellent.",
                "source": "twitter",
                "week": 1,
            },
            {
                "player_id": 1,
                "text": "I hate this awful performance. Terrible and disappointing.",
                "source": "twitter",
                "week": 1,
            },
        ]
    )

    assert len(results) == 2
    assert results[0]["player_id"] == 1
    assert results[0]["source"] == "twitter"
    assert results[0]["week"] == 1
    assert -1.0 <= results[0]["vader_score"] <= 1.0
    assert -1.0 <= results[1]["vader_score"] <= 1.0
    assert results[0]["vader_score"] > results[1]["vader_score"]
