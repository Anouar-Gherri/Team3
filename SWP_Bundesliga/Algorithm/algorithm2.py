import csv


def csv_lib_creator(library_name, crawler_data_file, delimiter=','):
    matches = list(csv.reader(crawler_data_file, delimiter=delimiter))
    if 'date' in matches[0]:
        del matches[0]  # skips the header

    teams_set = set()
    for row in matches:
        teams_set.add(row[1])
        teams_set.add(row[2])

    teams = list(teams_set)  # create list of unique teams

    # first list refers to total goals scored, second to totals games played
    teams_goals = {team: 0 for team in teams}
    teams_matches = {team: 0 for team in teams}

    for match in matches:
        team1 = match[1]
        team2 = match[2]
        goals_t1 = int(match[3])
        goals_t2 = int(match[4])

        teams_goals[team1] += goals_t1
        teams_goals[team2] += goals_t2
        teams_matches[team1] += 1
        teams_matches[team2] += 1

    teams_goals_per_match = \
        [[team, teams_goals[team] / teams_matches[team]] for team in teams]

    with open(library_name, 'w+', newline='') as lib_file:
        writer = csv.writer(lib_file)
        writer.writerows(teams_goals_per_match)
    lib_file.close()


def library_request(library, match_dict):
    reader = csv.reader(library)
    goals_per_match = {rows[0]: float(rows[1]) for rows in reader}

    host = match_dict['host']
    guest = match_dict['guest']

    if host not in goals_per_match:
        raise NameError("Couldn't find {} in the Library!".format(host))
    if guest not in goals_per_match:
        raise NameError("Couldn't find {} in the Library!".format(guest))

    gpm_host = goals_per_match[host]
    gpm_guest = goals_per_match[guest]

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

    result_dict = {'host': host}
    result_dict.update({case: res for case, res in zip(["win", "lose", "draw"], results)})

    return result_dict
