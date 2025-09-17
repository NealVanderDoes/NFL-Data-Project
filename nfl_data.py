import nfl_data_py as nfl


def team_names():
    teams = list(nfl.import_team_desc()['team_name'])
    return teams

#
# for i in nfl.import_team_desc():
#     print(i)

# print(team_names())