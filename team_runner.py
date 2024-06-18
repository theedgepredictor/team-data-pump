import json
import os

from espn_api_orm.league.api import ESPNLeagueAPI
from espn_api_orm.season.api import ESPNSeasonAPI
from espn_api_orm.team.api import ESPNTeamAPI
from espn_api_orm.consts import ESPNSportLeagueTypes

def main():
    root_path = './data'
    
    sport_league_pairs = list(ESPNSportLeagueTypes)
    sport_league_pairs = [
        ESPNSportLeagueTypes.FOOTBALL_NFL,
        ESPNSportLeagueTypes.FOOTBALL_COLLEGE_FOOTBALL,
        ESPNSportLeagueTypes.BASKETBALL_MENS_COLLEGE_BASKETBALL,
        ESPNSportLeagueTypes.BASKETBALL_NBA,
        ESPNSportLeagueTypes.BASKETBALL_WNBA,
        ESPNSportLeagueTypes.BASKETBALL_WOMENS_COLLEGE_BASKETBALL,
    ]
    for sport_league in sport_league_pairs:
        sport_str, league_str = sport_league.value.split('/')
        path = f'{root_path}/{sport_str}/{league_str}/'
        team_path = path + 'teams.json'
        teams = get_json_file(team_path)
        league_api = ESPNLeagueApi(sport_str, league_str)
        seasons = league_api.get_seasons()
        # get teams for season
        for season in seasons:
            team_season_path = f"{path}{season}.json"
            season_team = get_json_file(team_season_path)
            season_api = ESPNSeasonAPI(sport_str, league_str, season)
            team_ids = season_api.get_team_ids()
            for team_id in team_ids:
                team_api = ESPNTeamAPI(sport_str, league_str, season, team_id)
                team = team_api.get_team()
                # get each team
                # get team name
                # upsert season_teams
                # upsert teams
        
