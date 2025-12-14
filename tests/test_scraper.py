from lol_matches.scraper import MatchScraper

region = "europe"
match_id = 7638461064
scraper = MatchScraper(region)
match = scraper.get_match(match_id)


def test_scraper():
    assert isinstance(match, dict)


def test_match_parser():
    parsed = MatchScraper.parse_match_info(match)
    assert isinstance(parsed, dict)


def test_team_parser():
    parsed = MatchScraper.parse_teams(match)
    assert isinstance(parsed, list)


def test_participant_parser():
    parsed = MatchScraper.parse_participants(match)
    assert isinstance(parsed, list)
