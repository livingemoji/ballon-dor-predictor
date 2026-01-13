from sentiment.sentiment_pipeline import SentimentPipeline
from sentiment.save_sentiment import save_sentiments

pipeline = SentimentPipeline()

mock_posts = [
    {
        "player_id": 1,
        "text": "What a performance from Haaland, absolute monster!",
        "source": "twitter",
        "week": 1
    },
    {
        "player_id": 1,
        "text": "Invisible again in big matches...",
        "source": "twitter",
        "week": 1
    }
]

results = pipeline.process_posts(mock_posts)
save_sentiments(results)

print("Sentiment pipeline executed successfully.")
