import logging

from lol_matches.s3 import S3Helper
from lol_matches.scraper import MatchScraper
from lol_matches.settings import ScraperSettings

settings = ScraperSettings()


def create_objects(region):
    bucket_name = settings.s3_bucket_name
    s3 = S3Helper(bucket_name, region)
    scraper = MatchScraper(region)
    logging.info("Instanciated scraper and s3 objects")

    return s3, scraper


def scrape_match(match_id, scraper, s3):
    logging.info(f"Starting scraping match: {match_id}")
    match = scraper.get_match(match_id)

    logging.info(f"Parsing data for match: {match_id}")
    parsed_match = MatchScraper.parse_match_info(match)
    parsed_teams = MatchScraper.parse_teams(match)
    parsed_participants = MatchScraper.parse_participants(match)
    # print(parsed_match)

    logging.info(f"Saving match data at: {s3.s3_root}/")
    s3.save_dict(parsed_match, "match", match_id)
    s3.save_dict(parsed_teams, "team", match_id)
    s3.save_dict(parsed_participants, "participants", match_id)


def main():
    logging.basicConfig(
        filename="log/get-matches.log",
        format="%(asctime)s %(levelname)s:%(message)s",
        level=logging.INFO,
    )
    region = "europe"
    init_match_id = 7638461064
    match_id = init_match_id

    s3, scraper = create_objects(region)

    while True:
        try:
            scrape_match(match_id, scraper, s3)
        except Exception as e:
            logging.error(f"Couldn't scrape match: {match_id}")
        match_id += 1
