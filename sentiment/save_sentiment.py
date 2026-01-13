from db.database import SessionLocal
from db.models import Sentiment


def save_sentiments(sentiment_results):
    db = SessionLocal()

    for item in sentiment_results:
        sentiment = Sentiment(
            player_id=item["player_id"],
            text=item["text"],
            source=item["source"],
            week=item["week"],
            vader_score=item["vader_score"],
            llm_score=item["llm_score"]
        )

        db.add(sentiment)

    db.commit()
    db.close()
    print(f"Saved {len(sentiment_results)} sentiment records to the database.")


if __name__ == "__main__":
    save_sentiments([])  # Example call with empty list for testing purposes        
    print("Sentiment records saved successfully.")