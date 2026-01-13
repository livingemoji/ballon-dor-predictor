from typing import Dict, List
from .normalization import normalize_rating


COMPETITION_WEIGHTS = {
    "champions league": 1.5,
    "ucl": 1.5,
    "league": 1.0,
    "international": 1.4,
    "domestic cup": 0.7,
}


def get_competition_weight(competition: str) -> float:
    if not competition:
        return 1.0

    competition = competition.lower()
    return COMPETITION_WEIGHTS.get(competition, 1.0)


def aggregate_performance(match_ratings: List[Dict]) -> float:
    """
    match_ratings = [
      {
        "source": "sofascore",
        "rating": 8.4,
        "competition": "Champions League"
      }
    ]
    """

    if not match_ratings:
        return 0.0

    weighted_sum = 0.0
    total_weight = 0.0

    for entry in match_ratings:
        normalized = normalize_rating(
            entry["source"],
            entry["rating"]
        )

        competition_weight = get_competition_weight(
            entry.get("competition", "")
        )

        weighted_sum += normalized * competition_weight
        total_weight += competition_weight

    return weighted_sum / total_weight
