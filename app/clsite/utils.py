import random


def random_number_exponential_delay(pr=0.25, probability_of_none=0.0):
    if random.random() < probability_of_none:
        return 0

    i = 1
    while random.random() < pr:
        i += 1

    return i
