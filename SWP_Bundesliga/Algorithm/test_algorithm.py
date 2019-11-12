import pytest as pt
import AlgorithmClass as ac
import Algorithm as algo


@pytest.fixture
def create_RFA():
    RFAlgo = ac.Algorithm("RelativeFrequencyAlgorithm", algo.csv_lib_creator,
                          algo.csv_reader, '.csv', '.csv')
    return RFAlgo


#Algorithm class tests
@pytest.mark.AC
def test_AlgorithmClass_train_error1():
    RFA = create_RFA()
    with pytest.raises(ValueError):
        RFA.train('Library.csv', 'Data1.xls')

def test_AlgorithmClass_train_error2():
    RFA = create_RFA()
    with pytest.raises(ValueError):
        RFA.train('Library.xls', 'Data1.csv')

def test_AlgorithmClass_train_creation():
    RFA = create_RFA()
    with open('Data1.csv') as data:
        RFA.train('Library.csv', 'Data1.csv')
        with open('Library.csv') as Library:
            assert Library.read == data.read()

def test_AlgorithmClass_request_error1():
    RFA = create_RFA()
    with pytest.raises(NameError):
        RFA.request(dict(host='Munich', guest= 'Frankfurt'))

def test_AlgorithmClass_request():
    RFA = create_RFA()
    RFA.train('Library.csv', 'Data1.csv')
    assert RFA.request(dict(host='Munich', guest= 'Frankfurt')) \
           == dict(host= 'Munich', win= 0, lose= 0, draw = 1)



RFAlgo.train("Library.csv", 'Mappe1.csv')

def print_results(host, guest):
    print('Statistic for ' + host + ' against ' + guest +':')
    results = RFAlgo.request(dict(host=host, guest= guest))
    for (x,y) in results.items():
        print(x + ": " + str(y))

print_results('Munich', 'Duesseldorf')
print_results('Frankfurt', 'Duesseldorf')
print_results('Bavaria', 'Stuttgart')


