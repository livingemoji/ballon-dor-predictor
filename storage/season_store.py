from collections import defaultdict


class SeasonStore:
    def __init__(self):
        self.data = defaultdict(list)

    def add_week_score(self, player_name, week, score):
        self.data[player_name].append({
            "week": week,
            "score": score
        })

    def get_player_total(self, player_name):
        return sum(entry["score"] for entry in self.data[player_name])

    def get_all_players(self):
        return dict(self.data)
