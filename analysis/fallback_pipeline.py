from data_sources.google_discovery import discover_report_urls
from data_sources.report_scraper import scrape_report_text
from analysis.crucial_action_detector import detect_crucial_actions
from cache.simple_cache import get_cached, set_cache


def get_crucial_actions_for_player(player_name):
    urls = discover_report_urls(player_name)
    total_crucial_actions = 0

    for url in urls:
        cached = get_cached(url)
        if cached:
            text = cached
        else:
            text = scrape_report_text(url)
            if text:
                set_cache(url, text)

        total_crucial_actions += detect_crucial_actions(text)

    return total_crucial_actions
