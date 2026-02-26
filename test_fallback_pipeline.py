from analysis.fallback_pipeline import get_crucial_actions_for_player


def test_fallback_pipeline_handles_empty_scrape(monkeypatch):
    monkeypatch.setattr(
        "analysis.fallback_pipeline.discover_report_urls",
        lambda player_name: ["https://example.com/report-1"],
    )
    monkeypatch.setattr("analysis.fallback_pipeline.get_cached", lambda url: None)
    monkeypatch.setattr("analysis.fallback_pipeline.scrape_report_text", lambda url: "")

    actions = get_crucial_actions_for_player("Virgil van Dijk")

    assert actions == 0
