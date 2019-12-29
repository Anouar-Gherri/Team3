import pytest
import csv
from Algorithm import AlgorithmClass as aC
from Algorithm import algorithm1 as al1
from Algorithm import algorithm2_2 as al2_2


@pytest.fixture
def rfa():
    rfa = al1.create()
    return rfa


@pytest.fixture
def gpma2():
    gpma2 = al2_2.create()
    return gpma2


@pytest.mark.AlgorithmClass
def test_algorithm_creation(rfa, gpma2):
    assert rfa.name == "RelativeFrequencyAlgorithm"
    assert callable(rfa.request_function) is True
    assert callable(rfa.training_function) is True
    assert rfa.data_format == 'csv'
    assert rfa.trained is False
    assert rfa.library == []
    assert rfa.specifications == {'request_kwargs': {}, 'train_kwargs': {}}
    assert gpma2.specifications == {'request_kwargs': dict(kw_weight_team=0.5), 'train_kwargs': {}}

    rfa.train('TestData(2018).csv')
    assert rfa.trained is True


def test_algorithm_class_result_dict():
    host = 'Munich'
    results = [0, 0.2, 0.8]
    assert aC.results_to_dict(host, results) == dict(host='Munich', win=0, lose=0.2, draw=0.8)


def test_algorithm1_result_dict_error1():
    host = 'Munich'
    results = [0, 0, 0]  # not normalized
    results2 = [0, 'hello', 1]  # not numbers only
    results3 = [-1, 1, 1]  # not normalized
    with pytest.raises(ValueError):
        aC.results_to_dict(host, results)
        aC.results_to_dict(host, results2)
        aC.results_to_dict(host, results3)


# Checks whether the wrong file types are detected
def test_algorithm_class_train_error1(rfa):
    with pytest.raises(ValueError):
        rfa.train('TestData(2018).xls')  # ends with xls


# Checks whether a library is created
def test_algorithm_class_train_creation(rfa):
    rfa.train('TestData(2018).csv')
    assert rfa.library[0] == ['2018-08-24T20:30:00', 'FC Bayern', 'TSG 1899 Hoffenheim', 3, 1, 1]

    assert rfa.trained is True


# Checks whether requesting without training raises an Error
def test_algorithm_class_request_error1(rfa):
    with pytest.raises(NameError):
        rfa.request(dict(host='FC Bayern', guest='1899 Hoffenheim'))


# Checks whether the outcome is correct for an example
def test_algorithm_class_request(rfa):
    rfa.train('TestData(2018).csv')
    assert rfa.request(dict(host='FC Bayern', guest='Werder Bremen')) ==\
        dict(host='FC Bayern', win=1, lose=0, draw=0)


# Just visualisation. Uncomment below to see
def algorithm1_print_running():
    rfa = al1.create()

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
