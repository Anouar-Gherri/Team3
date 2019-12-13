from Algorithm import algorithm1 as al1
from Algorithm import algorithm2 as al2
from Algorithm import algorithm2_2 as al2_2


def create_algorithms():
    algorithms = [al.create() for al in [al1, al2, al2_2]]

    algorithm_dict = {al.name: al for al in algorithms}

    return algorithm_dict

# print(create_algorithms())
