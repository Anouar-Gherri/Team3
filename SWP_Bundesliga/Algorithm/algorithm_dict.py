from Algorithm import algorithm1 as al1
from Algorithm import algorithm2 as al2
from Algorithm import algorithm2_2 as al2_2
from Algorithm import algorithm3 as al3

algorithm_list = [al1, al2, al2_2, al3]


def create_algorithms() -> dict:
    """Creates a dictionary of all algorithms in algorithm_list

    :return: dictionary of algorithms
    """
    algorithms = [al.create() for al in algorithm_list]

    algorithm_dict = {al.name: al for al in algorithms}

    return algorithm_dict


def train_all(algorithm_dict, crawler_data_file_name) -> dict:
    """Trains all algorithms on the data file.

    :param algorithm_dict: An algorithm dictionary
    :param crawler_data_file_name: A data file name
    :return: A dictionary of the trained algorithms
    """
    algorithm_dict = {k: v.train(crawler_data_file_name)
                      for k, v in algorithm_dict.items()}
    return algorithm_dict

# print(create_algorithms())
