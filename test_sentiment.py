from sentiment.sentiment_pipeline import SentimentPipeline


def test_sentiment_pipeline_produces_scores_and_keeps_metadata():
    pipeline = SentimentPipeline()
    results = pipeline.process_posts(
        [
            {
                "player_id": 1,
                "text": "What a performance from Haaland, absolute monster!",
                "source": "twitter",
                "week": 1,
            },
            {
                "player_id": 1,
                "text": "Invisible again in big matches...",
                "source": "twitter",
                "week": 1,
            },
        ]
    )

    assert len(results) == 2
    assert results[0]["player_id"] == 1
    assert results[0]["source"] == "twitter"
    assert results[0]["week"] == 1
    assert results[0]["vader_score"] > results[1]["vader_score"]
