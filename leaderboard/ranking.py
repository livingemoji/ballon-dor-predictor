def rank_players(season_store):
    totals = []

    for player, weeks in season_store.get_all_players().items():
        total_score = sum(w["score"] for w in weeks)
        totals.append((player, round(total_score, 3)))

    totals.sort(key=lambda x: x[1], reverse=True)
    return totals
