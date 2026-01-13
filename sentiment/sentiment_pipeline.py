from typing import List, Dict
from .vader_analyzer import VaderSentimentAnalyzer


class SentimentPipeline:
    def __init__(self):
        self.vader = VaderSentimentAnalyzer()

    def process_posts(self, posts: List[Dict]) -> List[Dict]:
        """
        posts = [
          {
            "text": "...",
            "player_id": 1,
            "source": "twitter",
            "week": 3
          }
        ]
        """

        results = []

        for post in posts:
            vader_score = self.vader.analyze(post["text"])

            result = {
                "player_id": post["player_id"],
                "text": post["text"],
                "source": post["source"],
                "week": post["week"],
                "vader_score": vader_score,
                "llm_score": None  # Placeholder for later
            }

            results.append(result)

        return results
