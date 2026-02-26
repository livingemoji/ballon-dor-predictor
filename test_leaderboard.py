from storage.season_store import SeasonStore
from leaderboard.ranking import rank_players


def test_rank_players_sorts_by_total_score_desc():
    store = SeasonStore()
    store.add_week_score("Mbappe", 1, 0.78)
    store.add_week_score("Mbappe", 2, 0.81)
    store.add_week_score("Haaland", 1, 0.75)
    store.add_week_score("Haaland", 2, 0.73)
    store.add_week_score("Messi", 1, 0.69)

    ranking = rank_players(store)

    assert ranking[0] == ("Mbappe", 1.59)
    assert ranking[1] == ("Haaland", 1.48)
    assert ranking[2] == ("Messi", 0.69)
