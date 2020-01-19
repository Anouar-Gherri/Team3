from Algorithm import AlgorithmClass as aC


# --- Algorithm Functions ---
# Simply copies the csv crawler data into library-name.csv
def library_creator(matches, **kwargs):
    """Creates the Library.

    :param matches: the data file with the crawler data
    """

    return matches


# Request a prediction from the library
def library_reader(library, match_dict, **kwargs):
    """Request form the Library.

    :param library: a library file
    :param match_dict: a dictionary with match specifications

    :return: A list containing the predicted results for the host
    """

    host = match_dict["host"]
    guest = match_dict["guest"]
    # The result list stores the occurrences like this: [wins, losses, draws]
    results = [0, 0, 0]
    # more results case the teams played, but not against each other
    results_host = [0, 0, 0]
    results_guest = [0, 0, 0]

    # --- Library reading ---
    for data in library:
        # converts the lines in a list (assuming structure is [date, t1, t2, gt1, gt2])
        team1, team2, goals_t1, goals_t2 = data[1:5]
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
    # Case matches didn't occur
    if sum(results) <= 0:
        if sum(results_guest + results_host) > 0:  # if at least one team played a game
            results = [results_host[i] + results_guest[j]
                       for i, j in zip([0, 1, 2], [1, 0, 2])]
        else:
            results = [0, 0, 1]  # else return 100% draw

    return normalize(results)


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


def create():
    """Creates the RelativeFrequency-Algorithm

    :return: Algorithm (RelativeFrequency)
    """
    rfa = aC.Algorithm("RelativeFrequencyAlgorithm", library_creator,
                       library_reader, 'csv')
    return rfa