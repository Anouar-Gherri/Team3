# Creates the Functions for the Relative Frequency Algorithm

# --- Helper functions ---
# Creates a dictionary containing the normalized results
def result_dict(result_list, host):
    dict = {'host': host}
    result_list_normalized = [r / sum(result_list) for r in result_list]
    dict.update({case: res for case, res in zip(["win", "lose", "draw"], result_list_normalized)})
    return dict


# Returns who won the game ( 0 = host, 1 = guest, 2 = none )
def calculate_win(host, guest, team1, team2, goals_t1, goals_t2):
    if goals_t1 == goals_t2:
        return 2
    elif goals_t1 > goals_t2:
        return guest == team1
    else:
        return host == team1

    
# --- Algorithm Functions ---
# Simply copies the csv crawler data into library-name.csv
def csv_lib_creator(lib_name, crawler_data_file):
    with open(lib_name, "w+") as lib_file:
        for line in crawler_data_file:
            lib_file.write(line)
    lib_file.close()


# Request a prediction from the library
def csv_reader(match_dict, library, column_separator=";"):
    host = match_dict["host"]
    guest = match_dict["guest"]
    # The result list stores the occurences like this: [wins, losses, draws]
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
    # Case matches occured
    if sum(results) > 0:
        return result_dict(host, results)
    # else if at least one team played a game
    elif sum(results_guest + results_host) > 0:
        # Do some rule of thumb math
        pseudo_results = [results_host[i] + results_guest[j]
                          for i,j in zip([0, 1, 2], [1, 0, 2])]
        return result_dict(host, pseudo_results)
        # else return 100% draw
    else:
        pseudo_results = [0, 0, 1]
        return result_dict(host, pseudo_results)
