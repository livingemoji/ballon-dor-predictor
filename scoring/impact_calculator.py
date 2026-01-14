from positions.profiles import POSITION_PROFILES


class ImpactCalculator:
    def __init__(self, position: str):
        if position not in POSITION_PROFILES:
            message = (
                "Unknown position: "
                f"{position}"
            )
            raise ValueError(message)

        self.profile = POSITION_PROFILES[position]

    def compute_stat_score(self, stats: dict) -> float:
        """
        Example stats structure:

        {
            "goals": 1,
            "assists": 0,
            "defensive_actions": 5
        }
        """

        goals = stats.get(
            "goals",
            0,
        )
        assists = stats.get(
            "assists",
            0,
        )
        defensive_actions = stats.get(
            "defensive_actions",
            0,
        )

        score = 0.0

        score += (
            goals
            * self.profile["goal_weight"]
        )

        score += (
            assists
            * self.profile["assist_weight"]
        )

        score += (
            defensive_actions
            * self.profile["defensive_weight"]
        )

        return score

    def apply_crucial_actions(
        self,
        base_score: float,
        crucial_actions: int,
    ) -> float:
        """
        Crucial actions amplify impact.
        """

        if crucial_actions <= 0:
            return base_score

        multiplier = 1 + (
            crucial_actions
            * 0.1
        )

        return (
            base_score
            * multiplier
            * self.profile["crucial_multiplier"]
        )
