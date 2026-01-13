from scoring.aggregation import aggregate_performance


COMPETITION_WEIGHT = {
    "League": 1.0,
    "Champions League": 1.4,
    "International": 1.3,
    "Cup": 0.9
}


class WeeklyScoringEngine:
    def __init__(self, sentiment_weight=0.3, performance_weight=0.7):
        self.sentiment_weight = sentiment_weight
        self.performance_weight = performance_weight

    def compute_week_score(self, performances, sentiment_score):
        """
        performances: list of dicts
        sentiment_score: float [-1, 1]
        """

        weighted_performances = []

        for p in performances:
            weight = COMPETITION_WEIGHT.get(p["competition"], 1.0)
            weighted_performances.append({
                **p,
                "rating": p["rating"] * weight
            })

        performance_score = aggregate_performance(weighted_performances)

        final_score = (
            performance_score * self.performance_weight +
            sentiment_score * self.sentiment_weight
        )

        return round(final_score, 4)
