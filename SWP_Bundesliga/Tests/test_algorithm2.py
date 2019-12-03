import pytest
from Algorithm import AlgorithmClass as aC
from Algorithm import algorithm2 as al2


@pytest.fixture
def gpma():
    gpma = aC.Algorithm('GoalsPerMatchAlgorithm', al2.csv_lib_creator,
                        al2.library_request, 'csv', 'csv', 'GPMA')
    return gpma


@pytest.mark.al2
def test_algorithm2_running(gpma):
    gpma.train('TestData(2018).csv')

    assert gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg')) \
        == dict(host='Borussia Dortmund', win=0.8725490196078431, lose=0, draw=0.12745098039215685)

    assert gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg')) != \
        gpma.request(dict(host='SC Freiburg', guest='Borussia Dortmund'))


def test_algorithm2_request_error1(gpma):
    gpma.train('TestData(2018).csv')

    with pytest.raises(ValueError):
        gpma.request(dict(host='Borussia Dortmund', guest='Kein Team'))
        gpma.request(dict(host="Gibt's nicht", guest='SC Freiburg'))


def algorithm2_print_running():
    gpma = aC.Algorithm('GoalsPerMatchAlgorithm', al2.csv_lib_creator,
                        al2.library_request, 'csv', 'csv', 'GPMA')

    gpma.train('TestData(2018).csv')

    def print_results(host, guest):
        print('Statistic for ' + host + ' as host against ' + guest + ':')
        results = gpma.request(dict(host=host, guest=guest))
        for (x, y) in results.items():
            print(x + ": " + str(y))
        print()

    print_results('VfL Wolfsburg', 'Bayer Leverkusen')
    print_results('1. FSV Mainz 05', 'VfL Wolfsburg')
    print_results('Borussia Dortmund', 'SC Freiburg')


# Uncomment this to see some output
# algorithm2_print_running()
