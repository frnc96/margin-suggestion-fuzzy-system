import os
import numpy as np
import matplotlib.pyplot as plt
from src.fuzzy.Subset import FuzzySubset
from src.helpers.Global import LabelHelper as Lh


class FuzzySet:
    def __init__(self, name: str, x_min: float, x_max: float, step: float, x=None):
        self.name: str = name
        self.x_range: [float] = np.arange(x_min, x_max, step)
        self.subsets: [FuzzySubset] = []
        self.x: int = x

    def add_subset(self, fuzzy_subset: FuzzySubset):
        self.subsets.append(fuzzy_subset)

        return self

    def plot(self):
        # comment line below to plot MF
        return self

        plots_dir_path = os.path.abspath("../plots")
        fig, ax0 = plt.subplots()

        for subset in self.subsets:
            ax0.plot(
                self.x_range,
                subset.membership_range,
                linewidth=2,
                label=Lh.snake_case_to_label(subset.name),
            )

        ax0.set_title(Lh.snake_case_to_label(self.name))
        ax0.legend()
        plt.tight_layout()
        plt.savefig(
            os.path.join(plots_dir_path, f"{self.name}_membership_functions.png")
        )
        plt.show()

        return self
