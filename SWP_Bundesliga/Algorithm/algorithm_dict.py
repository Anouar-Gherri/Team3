from Algorithm import algorithm1 as al1
from Algorithm import algorithm2 as al2
from Algorithm import algorithm2_2 as al2_2
from Algorithm import algorithm3 as al3


def create_algorithms():
    algorithms = [al.create() for al in [al1, al2, al2_2, al3]]

    algorithm_dict = {al.name: al for al in algorithms}

    return algorithm_dict


def train_all(algorithm_dict, crawler_data_file_name):
    algorithm_dict = {k: v.train(crawler_data_file_name)
                      for k, v in algorithm_dict.items()}
    return algorithm_dict

# print(create_algorithms())
