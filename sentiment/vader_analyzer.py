from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class VaderSentimentAnalyzer:
    def __init__(self):
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze(self, text: str) -> float:
        """
        Returns compound sentiment score in range [-1, 1]
        """
        scores = self.analyzer.polarity_scores(text)
        return scores["compound"]
