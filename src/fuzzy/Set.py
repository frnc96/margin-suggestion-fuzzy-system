import numpy as np


class FuzzySet:
    def __init__(self, name: str, x_min: int, x_max: int):
        self.name = name
        self.x_range = np.arange(x_min, x_max, 1)

    def add_set(self, fuzzy_set):
        self.fuzzy_sets.append(fuzzy_set)
