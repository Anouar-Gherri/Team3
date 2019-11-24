import pytest
import Algorithm.AlgorithmClass as aC
import Algorithm.algortihm1 as al1


@pytest.fixture
def create_rfa():
    rfa = aC.Algorithm("RelativeFrequencyAlgorithm", al1.csv_lib_creator,
                       al1.csv_reader, '.csv', '.csv')
    return rfa


# Algorithm class tests
@pytest.mark.aC
def test_algorithm_class_train_error1():
    rfa = create_rfa()
    with pytest.raises(ValueError):
        rfa.train('Library.csv', 'Data1.xls')


def test_algorithm_class_train_error2():
    rfa = create_rfa()
    with pytest.raises(ValueError):
        rfa.train('Library.xls', 'Data1.csv')


def test_algorithm_class_train_creation():
    rfa = create_rfa()
    with open('Data1.csv') as data:
        rfa.train('Library.csv', 'Data1.csv')
        with open('Library.csv') as Library:
            assert Library.read == data.read()


def test_algorithm_class_request_error1():
    rfa = create_rfa()
    with pytest.raises(NameError):
        rfa.request(dict(host='Munich', guest='Frankfurt'))


def test_algorithm_class_request():
    rfa = create_rfa()
    rfa.train('Library.csv', 'Data1.csv')
    assert rfa.request(dict(host='Munich', guest='Frankfurt')) == dict(host='Munich', win=0, lose=0, draw=1)


@pytest.mark.al1
def test_algorithm1_result_dict():
    result_list = [0, 1, 4]
    host = 'Munich'
    assert al1.result_dict(result_list, host) == dict(host='Munich', win=0, lose=0.2, draw=0.8)


def test_algorithm1_result_dict_error1():
    result_list = [0, 0, 0]
    host = 'Munich'
    with pytest.raises(ValueError):
        al1.result_dict(result_list, host)


def test_algorithm1_calculate_win():
    host = 'Munich'
    guest = 'Dusseldorf'
    assert al1.calculate_win(host, guest, host, guest, 1, 0) == 0  # 0 == host wins
    assert al1.calculate_win(host, guest, host, guest, 0, 1) == 1  # 1 == guest wins
    assert al1.calculate_win(host, guest, host, guest, 0, 1) == 2  # 2 == draw


def test_algorithm1_calculate_win_error1():
    host = 'Munich'
    guest = 'Dusseldorf'
    team2 = 'Borussia'
    with pytest.raises(ValueError):
        al1.calculate_win(host, guest, host, team2, 1, 0)


# Missing: test for csv_reader and library_creator. They should work thou.


# other tests
def algorithm1_running_test():
    rfa = create_rfa()

    rfa.train("Library.csv", 'all_games_2018.csv')

    assert rfa.request({'host': 'Borussia Dortmund', 'guest': 'Hertha BSC'}) \
           == rfa.request({'host': 'Borussia Dortmund', 'guest': 'Hertha BSC'})


def algorithm1_print_running():
    rfa = aC.Algorithm("RelativeFrequencyAlgorithm", al1.csv_lib_creator,
                       al1.csv_reader, '.csv', '.csv')

    rfa.train("Library.csv", 'all_games_2018.csv')

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
