import numpy as np
import matplotlib.pyplot as plt
from src.fuzzy.Subset import FuzzySubset


class FuzzySet:
    def __init__(self, name: str, x_min: int, x_max: int, x=None):
        self.name: str = name
        self.x_range: [float] = np.arange(x_min, x_max, 1)
        self.subsets: [FuzzySubset] = []
        self.x: int = x

    def add_subset(self, fuzzy_subset: FuzzySubset):
        self.subsets.append(fuzzy_subset)

        return self
