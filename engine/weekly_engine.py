from scoring.aggregation import aggregate_performance
from scoring.impact_calculator import ImpactCalculator


class WeeklyScoringEngine:
    def __init__(self, sentiment_weight=0.3, performance_weight=0.7):
        self.sentiment_weight = sentiment_weight
        self.performance_weight = performance_weight

    def compute_week_score(
        self,
        performances,
        sentiment_score,
        position,
        stats,
        crucial_actions
    ):
        impact_calc = ImpactCalculator(position)

        performance_score = aggregate_performance(performances)

        stat_score = impact_calc.compute_stat_score(stats)
        stat_score = impact_calc.apply_crucial_actions(
            stat_score, crucial_actions
        )

        final_score = (
            performance_score * self.performance_weight +
            stat_score * 0.4 +
            sentiment_score * self.sentiment_weight
        )

        return round(final_score, 4)
