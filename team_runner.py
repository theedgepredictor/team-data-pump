import json
import os

from espn_api_orm.season.api import ESPNSeasonAPI
from espn_api_orm.team.api import ESPNTeamAPI
from espn_api_orm.league.api import ESPNLeagueAPI
from espn_api_orm.consts import ESPNSportLeagueTypes

from src.utils import get_json_file, put_json_file, get_value


def make_team(team):
    id = team.slug
    print('Making Team: ', id)
    return {
        'id': id,
        'franchiseId': team.id,
        'guid': team.guid,
        'uid': team.uid,
        'alternateIds': team.alternateIds,
        'location': team.location.strip() if team.location else None,
        'name': team.name.strip() if team.name else None,
        'nickname': team.nickname.strip() if team.nickname else None,
        'abbreviation': team.abbreviation.strip() if team.abbreviation else None,
        'displayName': team.displayName.strip() if team.displayName else None,
        'shortDisplayName': team.shortDisplayName.strip() if team.shortDisplayName else None,
        'color': team.color.strip() if team.color else None,
        'alternateColor': team.alternateColor.strip() if team.alternateColor else None,
        'logo': team.logos[0].href if team.logos else None,
        'altLogo': team.logos[1].href if team.logos else None,
        'isActive': team.isActive,
        'isAllStar': team.isAllStar,
        'college': team.college.strip() if isinstance(team.college, str) else (get_value("http://sports.core.api.espn.com/v2/colleges",team.college) if isinstance(team.college, dict) else None),
        'venueId': team.venue.id if team.venue else None,
    }


def make_season_team(season_team, season):
    return {
        'id': f"{season}-{season_team.id}",
        'teamId': season_team.slug,
        'franchiseId': season_team.id,
        'season': season
    }


def main():
    root_path = './data'

    sport_league_pairs = list(ESPNSportLeagueTypes)
    sport_league_pairs = [
        ESPNSportLeagueTypes.FOOTBALL_NFL,
        ESPNSportLeagueTypes.FOOTBALL_COLLEGE_FOOTBALL,
    ]
    for sport_league in sport_league_pairs:
        sport_str, league_str = sport_league.value.split('/')
        path = f'{root_path}/{sport_str}/{league_str}/'
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)

        # Get existing teams for sport league
        teams_path = path + 'teams.json'
        existing_teams = get_json_file(teams_path)
        league_api = ESPNLeagueAPI(sport_str, league_str)

        # Get new teams
        existing_franchise_ids = [i['franchiseId'] for i in existing_teams] if existing_teams != {} else []
        franchise_ids = league_api.get_franchises()
        new_franchise_ids = list(set(franchise_ids) - set(existing_franchise_ids))
        new_franchise_ids = sorted(new_franchise_ids)

        print(f"Getting {len(new_franchise_ids)} new franchises for: {league_str} {sport_str}")

        teams = league_api.get_teams(new_franchise_ids)
        teams = [make_team(i) for i in teams]
        if existing_teams != {}:
            for existing_team in existing_teams:
                if existing_team['franchiseId'] not in new_franchise_ids:
                    teams.append(existing_team)
        # Create an id to franchiseId dict mapper to define all teams in league
        team_dict = {i['id']: i['franchiseId'] for i in teams}

        # Get latest season
        seasons = sorted([i for i in league_api.get_seasons() if i > 2001])
        for season in sorted(seasons, reverse=True):
            team_season_path = f"{path}{season}/teams.json"
            season_teams = get_json_file(team_season_path)
            if season_teams != {}:
                seasons = list(range(season, seasons[-1] + 1))
                break

        print(f"Running for seasons: {seasons[0]}-{seasons[-1]}")
        # get teams for seasons
        for season in seasons:
            print("*" * 20)
            print(f"Season: {season}")
            print("*" * 20)
            print()
            # define the season api
            season_api = ESPNSeasonAPI(sport_str, league_str, season)
            if not os.path.exists(path + str(season)):
                os.makedirs(path + str(season), exist_ok=True)

            # Get existing teams for season for the sport league
            team_season_path = f"{path}{season}/teams.json"
            existing_season_teams = get_json_file(team_season_path)
            new_season_teams = []
            existing_season_team_ids = [i['teamId'] for i in existing_season_teams] if existing_season_teams != {} else []

            # Get new teams for season
            season_team_ids = season_api.get_team_season_ids()
            new_season_team_ids = list(set(season_team_ids) - set(existing_season_team_ids))
            new_season_team_ids = sorted(new_season_team_ids)
            print(f'Getting {len(new_season_team_ids)} team records for the {season} season...')
            for team_id in new_season_team_ids:
                # define team api
                team_api = ESPNTeamAPI(sport_str, league_str, season, team_id)
                team_obj = team_api.get_team()
                new_season_team = make_season_team(team_obj, season)
                new_season_teams.append(new_season_team)

                # If team doesn't exist, add it to the teams list and add it to the team dict
                if team_obj.slug not in team_dict:
                    teams.append(make_team(team_obj))
                    team_dict[team_obj.slug] = team_id

            # Write new season teams to file
            put_json_file(team_season_path, new_season_teams)

        # Write teams to file
        put_json_file(teams_path, teams)

if __name__ == "__main__":
    main()