from traceback import print_exc

from riotwatcher import LolWatcher

from lol_matches.settings import ScraperSettings
from lol_matches.utils import safe_get

settings = ScraperSettings()


class MatchScraper:
    def __init__(self, region: str) -> None:
        region_prefix = {"europe": "EUW1_"}
        self.region = region
        self.region_prefix = region_prefix.get(self.region)
        self.api_key = settings.riot_api_key

        try:
            self.watcher = LolWatcher(self.api_key)
        except:
            print_exc()

    def get_match(self, match_id: int):
        match_id = f"{self.region_prefix}{match_id}"
        try:
            match = self.watcher.match.by_id(self.region, match_id)
        except:
            match = {"message": "error"}
            print_exc()
        return match

    def parse_match_info(match: dict):
        metadata_keys = ["matchId"]
        info_keys = [
            "gameId",
            "platformId",
            "queueId",
            "gameDuration",
            "gameCreation",
            "gameStartTimestamp",
            "gameVersion",
            "mapId",
        ]
        metadata_dict = {k: match["metadata"][k] for k in metadata_keys}
        info_dict = {k: match["info"][k] for k in info_keys}
        return {**metadata_dict, **info_dict}

    def parse_base_info(match: dict):
        match_id = safe_get(match, "metadata", "matchId")
        game_id = safe_get(match, "info", "gameId")
        return {"matchId": match_id, "gameId": game_id}

    def parse_participants(match: dict):
        base_info = MatchScraper.parse_base_info(match)
        participants = match["info"]["participants"]
        part_keys = [
            "kills",
            "deaths",
            "assists",
            "champExperience",
            "damageDealtToObjectives",
            "damageDealtToTurrets",
            "damageSelfMitigated",
            "itemsPurchased",
            "longestTimeSpentLiving",
            "totalDamageDealt",
            "totalDamageDealtToChampions",
            "totalDamageShieldedOnTeammates",
            "totalDamageTaken",
            "totalHeal",
            "totalHealsOnTeammates",
            "totalMinionsKilled",
            "doubleKills",
            "tripleKills",
            "quadraKills",
            "pentaKills",
            "teamId",
            "goldEarned",
        ]
        parsed = list()

        for part in participants:
            part_id = {"participantId": part["participantId"]}
            part_dict = {k: part[k] for k in part_keys}
            parsed.append({**base_info, **part_id, **part_dict})

        return parsed

    def parse_teams(match: dict):
        base_info = MatchScraper.parse_base_info(match)
        teams = match["info"]["teams"]
        parsed = list()

        for team in teams:
            team_id = {"teamId": team["teamId"], "win": team["win"]}
            team_dict = {
                "baron_kill": safe_get(team, "objectives", "baron", "kills"),
                "baron_first": safe_get(team, "objectives", "baron", "first"),
                "champion_kill": safe_get(team, "objectives", "champion", "kills"),
                "champion_first": safe_get(team, "objectives", "champion", "first"),
                "dragon_kill": safe_get(team, "objectives", "dragon", "kills"),
                "dragon_first": safe_get(team, "objectives", "dragon", "first"),
                "inhibitor_kill": safe_get(team, "objectives", "inhibitor", "kills"),
                "inhibitor_first": safe_get(team, "objectives", "inhibitor", "first"),
                "riftHerald_kill": safe_get(team, "objectives", "riftHerald", "kills"),
                "riftHerald_first": safe_get(team, "objectives", "riftHerald", "first"),
                "tower_kill": safe_get(team, "objectives", "tower", "kills"),
                "tower_first": safe_get(team, "objectives", "tower", "first"),
            }
            parsed.append({**base_info, **team_id, **team_dict})

        return parsed
