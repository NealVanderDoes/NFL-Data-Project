import nfl_data_py as nfl
import pandas as pd


def team_names() -> list[str]:
    """
    Generate a sorted and modified list of unique current NFL team names.

    :return: A customized sorted list of unique current NFL team names.
    :rtype: list[str]
    """
    teams = sorted(list(set(nfl.import_team_desc()['team_name'])))
    teams[16], teams[18] = teams[18], teams[16]
    teams.pop(25)
    teams.pop(27)
    teams.pop(29)
    teams[27], teams[28] = teams[28], teams[27]
    return teams

def years() -> list[str]:
    """
    Generates a list of years in descending order from 2024 to 1999 as strings.

    :return: A list of years as strings, ordered from 2024 to 1999
    :rtype: list[str]
    """
    nfl_years = []

    stat_years = list(range(1999, 2025))
    stat_years.sort(reverse=True)

    for i in stat_years:
        nfl_years.append(str(i))

    return nfl_years

def weekly_data(year: int, team: str) -> pd.DataFrame:
    """
    Fetches weekly player performance data for a given NFL team and year.

    :param year: The year for which the data is to be fetched.
    :type year: int
    :param team: The team name whose data is to be filtered from the weekly stats.
    :type team: str
    :return: A Pandas DataFrame containing the weekly performance data of players from the
        specified team.
    :rtype: pandas.DataFrame
    """
    data = nfl.import_weekly_data([year],
                                  columns=['player_name', 'position', 'recent_team', 'season',
                                           'week', 'opponent_team', 'completions', 'attempts', 'passing_yards',
                                           'passing_tds', 'interceptions', 'sacks', ], downcast=False)

    data.set_index('recent_team', inplace=True)
    data = data.loc[team]
    return data