from storage.season_store import SeasonStore
from leaderboard.ranking import rank_players

store = SeasonStore()

store.add_week_score("Mbappe", 1, 0.78)
store.add_week_score("Mbappe", 2, 0.81)

store.add_week_score("Haaland", 1, 0.75)
store.add_week_score("Haaland", 2, 0.73)

store.add_week_score("Messi", 1, 0.69)

ranking = rank_players(store)

for i, (player, score) in enumerate(ranking, 1):
    print(f"{i}. {player} — {score}")
