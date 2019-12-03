import csv


def csv_lib_creator(library_name, crawler_data_file, delimiter_=','):
    matches = list(csv.reader(crawler_data_file, delimiter=delimiter_))
    if 'date' in matches[0]:
        del matches[0]  # skips the header

    # create list of unique teams
    teams_set = set()
    for row in matches:
        teams_set.add(row[1])
        teams_set.add(row[2])
    teams = list(teams_set)

    team_stats = {team: [0, 0] for team in teams}  # {team: [total goals, total games]}
    home_away_goals = [0, 0]  # [total goals home, total goals away]

    for match in matches:
        # takes first host (i = 1), then guest (i = 2). i+2 are the according goals
        for i in [1, 2]:
            team = match[i]
            goals = int(match[i + 2])

            team_stats[team][0] += goals
            team_stats[team][1] += 1

            home_away_goals[i == 2] += goals

    teams_gpm = [[team, team_stats[team][0] / team_stats[team][1]] for team in teams]

    home_away_gpm = [['home_gpm', home_away_goals[0] / len(matches)],
                     ['away_gpm', home_away_goals[1] / len(matches)]]

    with open(library_name, 'w+', newline='') as lib_file:
        writer = csv.writer(lib_file)
        writer.writerows(teams_gpm)
        writer.writerows(home_away_gpm)
    lib_file.close()

    return teams_set


def library_request(library, match_dict):
    reader = csv.reader(library)
    goals_per_match = {rows[0]: float(rows[1]) for rows in reader}

    host = match_dict['host']
    guest = match_dict['guest']

    gpm_home, gpm_away = goals_per_match['home_gpm'], goals_per_match['away_gpm']

    gpm_host = 0.75 * goals_per_match[host] + 0.25 * gpm_home
    gpm_guest = 0.75 * goals_per_match[guest] + 0.25 * gpm_away

    results = [0, 0, 0]

    diff = abs(gpm_host - gpm_guest)

    if diff < 1:
        results[2] = 1 - diff
        if gpm_host > gpm_guest:
            results[0] = diff
        else:
            results[1] = diff
    elif gpm_host > gpm_guest:
        results[0] += 1
    else:
        results[1] += 1

    return results
