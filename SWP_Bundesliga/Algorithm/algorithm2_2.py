from Algorithm import algorithm2 as al2


def create():
    """Creates the GoalsPerMatch-Algorithm with adjusting for playing at home/away.

    :return: Algorithm (GoalsPerMatch with attention to home/away)
    """
    return al2.gpma_base('GoalsPerMatchAlgorithmV2', 'GPMA_V2', 0.5)
