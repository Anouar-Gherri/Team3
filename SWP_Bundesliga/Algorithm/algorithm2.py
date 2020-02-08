from Algorithm import AlgorithmClass as aC


def library_creator(matches, **kwargs):
    """Creates the Library.

    :param matches: the data file with the crawler data
    :param kwargs:
    :return: a List containing each teams goals per match
    """

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

    teams_gpm.extend(home_away_gpm)

    return teams_gpm


def library_request(library, match_dict, weight_team=1, **kwargs):
    """Request form the Library.

    :param library: a library file
    :param match_dict: a dictionary with match specifications
    :param weight_team: The proportion (1 = 100%) of team GPM vs Home-Away GPM.
    :return: A list containing the predicted results for the host
    """
    if weight_team is library_request.__defaults__[0] and 'kw_weight_team' in kwargs:
        weight_team = kwargs['kw_weight_team']

    goals_per_match = {rows[0]: float(rows[1]) for rows in library}

    host = match_dict['host']
    guest = match_dict['guest']

    gpm_home, gpm_away = goals_per_match['home_gpm'], goals_per_match['away_gpm']

    weight_place = 1 - weight_team

    gpm_host = weight_team * goals_per_match[host] + weight_place * gpm_home
    gpm_guest = weight_team * goals_per_match[guest] + weight_place * gpm_away

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


def gpma_base(name, *args):
    gpma = aC.Algorithm(name, library_creator, library_request, 'csv')

    if args:
        gpma.set_request_specifications(dict(kw_weight_team=args[0]))

    return gpma


def create():
    """Creates the GoalsPerMatch-Algorithm

    :return: Algorithm (GoalsPerMatch)
    """
    return gpma_base('GoalsPerMatchAlgorithm')
