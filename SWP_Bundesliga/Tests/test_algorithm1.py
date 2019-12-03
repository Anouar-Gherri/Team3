import pytest
from Algorithm import AlgorithmClass as aC
from Algorithm import algorithm1 as al1


@pytest.fixture
def rfa():
    rfa = aC.Algorithm("RelativeFrequencyAlgorithm", al1.csv_lib_creator,
                       al1.csv_reader, '.csv', '.csv', 'RFA')
    return rfa


@pytest.mark.algorithm1
def test_algorithm1_fun_calculate_win():
    host = 'Munich'
    guest = 'Dusseldorf'
    assert al1.calculate_win(host, guest, host, guest, 1, 0) == 0  # 0 == host wins
    assert al1.calculate_win(host, guest, host, guest, 0, 1) == 1  # 1 == guest wins
    assert al1.calculate_win(host, guest, host, guest, 1, 1) == 2  # 2 == draw


def test_algorithm1_fun_calculate_win_error1():
    host = 'Munich'
    guest = 'Dusseldorf'
    team2 = 'Borussia'
    with pytest.raises(ValueError):
        al1.calculate_win(host, guest, host, team2, 1, 0)


# Basically, this has been covered in the AlgorithmClass tests
# def test_algorithm1_runs():
#    pass


def test_algorithm1_returns_dict(rfa):
    rfa.train('TestData(2018).csv')

    assert type(rfa.request({'host': 'Borussia Dortmund', 'guest': 'Hertha BSC'})) is dict


def algorithm1_print_running():
    rfa = aC.Algorithm("RelativeFrequencyAlgorithm", al1.csv_lib_creator,
                       al1.csv_reader, 'csv', 'csv', 'RFA')

    rfa.train('TestData(2018).csv')

    def print_results(host, guest):
        print('Statistic for ' + host + ' against ' + guest + ':')
        results = rfa.request(dict(host=host, guest=guest))
        for (x, y) in results.items():
            print(x + ": " + str(y))
        print()

    print_results('Borussia Dortmund', 'SC Freiburg')
    print_results('SC Freiburg', 'FC Bayern')

# Uncomment this to see some output
# algorithm1_print_running()
