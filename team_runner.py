import json
import os

from espn_api_orm.league.api import ESPNLeagueAPI
from espn_api_orm.season.api import ESPNSeasonAPI
from espn_api_orm.team.api import ESPNTeamAPI
from espn_api_orm.consts import ESPNSportLeagueTypes

def main():
    root_path = './data'
    team_path = root_path + '/' + 'teams.json'
    teams = get_json_file(team_path)

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
        league_api = ESPNLeagueApi()
        seasons = league_api.get_seasons()
        # get teams for season
        # get each team
        # get team name
        
