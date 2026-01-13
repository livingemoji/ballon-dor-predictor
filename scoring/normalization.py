def min_max_normalize(
    value: float, min_value: float, max_value: float
) -> float:
    """
    Normalize a value to range [0, 1]
    """
    if max_value == min_value:
        return 0.0
    return (value - min_value) / (max_value - min_value)


def normalize_rating(source: str, rating: float) -> float:
    """
    Normalizes ratings from different platforms to [0, 1]
    """

    source_ranges = {
        "sofascore": (6.0, 10.0),
        "fotmob": (5.0, 10.0),
        "flashscore": (5.0, 10.0),
    }

    if source.lower() not in source_ranges:
        raise ValueError(f"Unknown rating source: {source}")

    min_val, max_val = source_ranges[source.lower()]
    return min_max_normalize(rating, min_val, max_val)
