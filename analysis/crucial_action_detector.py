CRUCIAL_KEYWORDS = [
    "goal-line clearance",
    "last-ditch tackle",
    "penalty save",
    "blocked on the line",
    "crucial save",
    "one-on-one save",
    "saved a penalty",
    "cleared off the line",
    "vital interception",
    "game-changing tackle"
]


def detect_crucial_actions(text):
    """
    Counts occurrences of crucial football actions.
    """

    count = 0
    for keyword in CRUCIAL_KEYWORDS:
        count += text.count(keyword)

    return count
