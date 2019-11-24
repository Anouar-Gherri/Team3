import pytest
import Algorithm.AlgorithmClass as aC
import Algorithm.algorithm2 as al2


@pytest.fixture
def create_gpma():
    gpma = aC.Algorithm('GoalsPerMatchAlgorithm', al2.csv_lib_creator,
                        al2.library_request, '.csv', '.csv')
    return gpma


@pytest.mark.al2
def algorithm2_running_test():
    gpma = create_gpma()

    gpma.train('Library.csv', 'all_games_2018.csv')

    assert gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg')) \
           == dict(host='Borussia Dortmund', win=1, lose=0, draw=0)


def algorithm2_request_error1():
    gpma = create_gpma()

    gpma.train('Library.csv', 'all_games_2018.csv')

    with pytest.raises(NameError):
        gpma.request(dict(host='Borussia Dortmund', guest='Kein Team'))
        gpma.request(dict(host="Gibt's nicht", guest='SC Freiburg'))


def algorithm2_print_running():
    gpma = aC.Algorithm('Goals_per_match_Algorithm', al2.csv_lib_creator,
                        al2.library_request, '.csv', '.csv')

    gpma.train("Library.csv", 'all_games_2018.csv')

    def print_results(host, guest):
        print('Statistic for ' + host + ' against ' + guest + ':')
        results = gpma.request(dict(host=host, guest=guest))
        for (x, y) in results.items():
            print(x + ": " + str(y))
        print()

    print_results('VfL Wolfsburg', 'Fortuna Düsseldorf')
    print_results('Borussia Dortmund', 'SC Freiburg')

# Uncomment this to see some output
# algorithm2_print_running()
