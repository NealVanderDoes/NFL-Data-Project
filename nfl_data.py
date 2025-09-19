import nfl_data_py as nfl


def team_names():
    teams = list(nfl.import_team_desc()['team_name'])
    return teams

def years():
    nfl_years = []

    stat_years = list(range(1999, 2025))
    stat_years.sort(reverse=True)

    for i in stat_years:
        nfl_years.append(str(i))

    return nfl_years

def weekly_data(year: int):
    data = nfl.import_weekly_data([year],
                                  columns=['player_name', 'position', 'recent_team', 'season',
                                           'week', 'opponent_team', 'completions', 'attempts', 'passing_yards',
                                           'passing_tds', 'interceptions', 'sacks', ])
    return data



# # Shows team description categories and the Team Names
# for i in nfl.import_team_desc():
#     print(i)
#
# print(team_names())