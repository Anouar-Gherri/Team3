import pytest
from Algorithm import algorithm3 as al3


@pytest.fixture
def pa():
    pa = al3.create()
    return pa


@pytest.mark.poisson_algorithm
def test_creation(pa):
    assert pa.name == 'PoissonAlgorithm'
    assert pa.trained is False
    assert pa.data_format == 'csv'


def test_running(pa):
    pa.train('Testdata(2018).csv')
    assert pa.request(dict(host='VfL Wolfsburg', guest='Bayer Leverkusen')) \
        == dict(host='VfL Wolfsburg', win=0.4629, lose=0.3229, draw=0.2142)


def algorithm3_print_running():
    pa = al3.create()

    pa.train('Testdata(2018).csv')

    def print_results(host, guest):
        print('Statistic for ' + host + ' as host against ' + guest + ':')
        results = pa.request(dict(host=host, guest=guest))
        for (x, y) in results.items():
            print(x + ": " + str(y))
        print()

    print_results('VfL Wolfsburg', 'Bayer Leverkusen')
    print_results('1. FSV Mainz 05', 'VfL Wolfsburg')
    print_results('Borussia Dortmund', 'SC Freiburg')
    print_results('SC Freiburg', 'Borussia Dortmund')

algorithm3_print_running()
