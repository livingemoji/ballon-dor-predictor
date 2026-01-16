from analysis.fallback_pipeline import get_crucial_actions_for_player

player = "Virgil van Dijk"

actions = get_crucial_actions_for_player(player)

print(f"Detected crucial actions for {player}:", actions)
