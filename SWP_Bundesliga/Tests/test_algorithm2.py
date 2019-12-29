import pytest
from Algorithm import algorithm2 as al2
from Algorithm import algorithm2_2 as al2_2


@pytest.fixture
def gpma():
    gpma = al2.create()
    return gpma


@pytest.fixture
def gpma2():
    gpma2 = al2_2.create()
    return gpma2


@pytest.mark.al2
def test_algorithm2_running(gpma, gpma2):
    gpma.train('TestData(2018).csv')
    gpma2.train('TestData(2018).csv')

    assert gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg'), 0.75) \
        == dict(host='Borussia Dortmund', win=0.8725490196078431, lose=0, draw=0.12745098039215685)

    assert gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg'), 1) != \
        gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg'), 0.9)

    assert gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg'), 1) == \
        gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg'))

    assert gpma.request(dict(host='Borussia Dortmund', guest='SC Freiburg'), 0.5) == \
        gpma2.request(dict(host='Borussia Dortmund', guest='SC Freiburg'))


def algorithm2_print_running():
    gpma = al2.create()

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
    print_results('SC Freiburg', 'Borussia Dortmund')


# Uncomment this to see some output
# algorithm2_print_running()
