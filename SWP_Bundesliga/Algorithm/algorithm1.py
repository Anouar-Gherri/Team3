# Creates the Functions for the Relative Frequency Algorithm
import csv


# --- Helper functions ---
# Creates a dictionary containing the normalized results
def normalize(result_list):
    if sum(result_list) < 1:
        raise ValueError('The result_list contains no results')
    result_list_normalized = [r / sum(result_list) for r in result_list]
    return result_list_normalized


# Returns who won the game ( 0 = host, 1 = guest, 2 = none )
def calculate_win(host, guest, team1, team2, goals_t1, goals_t2):
    if not {host, guest} == {team1, team2}:
        raise ValueError("host or guest didn't play in the match!" +
                         "(host: {}, guest: {}, team1: {}, team2: {})".format(host, guest, team1, team2))
    if goals_t1 == goals_t2:
        return 2
    elif goals_t1 > goals_t2:
        return guest == team1
    else:
        return host == team1


# --- Algorithm Functions ---
# Simply copies the csv crawler data into library-name.csv
# Also creates a set of the unique teams
def csv_lib_creator(lib_name, crawler_data_file, delimiter_=','):
    """

    :param lib_name: The filename of the Library
    :param crawler_data_file:
    :param delimiter_:
    :return:
    """
    # read the data file into a list
    matches = list(csv.reader(crawler_data_file, delimiter=delimiter_))

    # skips the header
    if 'date' in matches[0]:
        del matches[0]

    # get the set of unique teams
    teams_set = set()
    for row in matches:
        teams_set.add(row[1])
        teams_set.add(row[2])

    # and write the library
    with open(lib_name, "w+", newline='') as lib_file:
        writer = csv.writer(lib_file)
        writer.writerows(matches)
    lib_file.close()

    return teams_set


# Request a prediction from the library
def csv_reader(library, match_dict, column_separator=","):
    host = match_dict["host"]
    guest = match_dict["guest"]
    # The result list stores the occurrences like this: [wins, losses, draws]
    results = [0, 0, 0]
    # more results case the teams played, but not against each other
    results_host = [0, 0, 0]
    results_guest = [0, 0, 0]

    # --- Library reading ---
    for line in library:
        # converts the lines in a list (assuming structure is [date, t1, t2, gt1, gt2])
        data = line.strip().split(column_separator)
        team1 = data[1]
        team2 = data[2]
        goals_t1 = data[3]
        goals_t2 = data[4]
        # If host and guest played in this match
        if {team1, team2} == {host, guest}:
            # Calculate the results and increment
            # the equivalent slot in the results list
            results[calculate_win(host, guest, team1, team2, goals_t1,
                                  goals_t2)] += 1
        elif host in {team1, team2}:
            if host == team1:
                other = team2
            else:
                other = team1
            results_host[calculate_win(host, other, team1, team2, goals_t1,
                                       goals_t2)] += 1
        elif guest in {team1, team2}:
            if guest == team1:
                other = team2
            else:
                other = team1
            results_guest[calculate_win(guest, other, team1, team2, goals_t1,
                                        goals_t2)] += 1

    # --- Calculating Probabilities ---
    # Case matches occurred
    if sum(results) > 0:
        return normalize(results)
    # else if at least one team played a game
    elif sum(results_guest + results_host) > 0:
        # Do some rule of thumb math
        pseudo_results = [results_host[i] + results_guest[j]
                          for i, j in zip([0, 1, 2], [1, 0, 2])]
        return normalize(pseudo_results)
        # else return 100% draw
    else:
        pseudo_results = [0, 0, 1]
        return normalize(pseudo_results)
