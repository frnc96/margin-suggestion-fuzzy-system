import os
import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
import skfuzzy.membership as mf
from src.fuzzy.Set import FuzzySet
from src.fuzzy.Rule import FuzzyRule
from src.fuzzy.Subset import FuzzySubset


def plot_output(out_set: FuzzySet, out_margin: float, defuzzified: float, result: [float]):
    plots_dir_path = os.path.abspath("../plots")
    risk0 = np.zeros_like(out_set.x_range)
    fig, ax0 = plt.subplots()
    colors = ['r', 'g', 'b', 'y', 'm']

    color_index = 0
    for subset in out_set.subsets:
        ax0.plot(
            out_set.x_range,
            subset.membership_range,
            colors[color_index],
            linestyle='--',
            label=subset.name
        )
        color_index += 1

    ax0.fill_between(out_set.x_range, risk0, out_margin, facecolor='Orange', alpha=0.7)
    ax0.plot([defuzzified, defuzzified], [0, result], 'k', linewidth=3, alpha=0.9)

    ax0.set_title('Output Margin Area')
    plt.tight_layout()
    ax0.legend()
    plt.savefig(
        os.path.join(
            plots_dir_path,
            f'{out_set.name}_output.png'
        )
    )
    plt.show()


class FuzzyInferenceSystem:
    def __init__(self):
        self.fuzzy_sets: [FuzzySet] = []
        self.rules: [FuzzyRule] = []
        self.out_fuzzy_set = None

    def add_set(self, name: str, x_min: float, x_max: float, x: float, step: float = 1):
        self.fuzzy_sets.append(
            FuzzySet(name, x_min, x_max, step, x)
        )

        return self

    def add_out_set(self, name: str, x_min: float, x_max: float, step: float = 1):
        self.out_fuzzy_set = FuzzySet(name, x_min, x_max, step)

        return self

    def add_subset(self, name: str, set_name: str, membership_range: [float], mf_type: str = "trapezoidal"):
        for fuzzy_set in self.fuzzy_sets:
            if fuzzy_set.name == set_name:
                if mf_type == "trapezoidal":
                    membership_function = mf.trapmf(fuzzy_set.x_range, membership_range)
                elif mf_type == "triangular":
                    membership_function = mf.trimf(fuzzy_set.x_range, membership_range)
                else:
                    raise Exception(f"Membership function of type {mf_type} does not exist or is not supported!")

                membership_degree = fuzz.interp_membership(fuzzy_set.x_range, membership_function, fuzzy_set.x)

                fuzzy_set.add_subset(
                    FuzzySubset(
                        name=name,
                        membership_degree=membership_degree,
                        membership_range=membership_function
                    )
                )
                break

        return self

    def add_out_subset(self, name: str, membership_range: [float], mf_type: str = "trapezoidal"):
        if mf_type == "trapezoidal":
            membership_function = mf.trapmf(self.out_fuzzy_set.x_range, membership_range)
        elif mf_type == "triangular":
            membership_function = mf.trimf(self.out_fuzzy_set.x_range, membership_range)
        else:
            raise Exception(f"Membership function of type {mf_type} does not exist or is not supported!")

        self.out_fuzzy_set.add_subset(
            FuzzySubset(name=name, membership_degree=membership_function, membership_range=membership_function)
        )

        return self

    def add_rule(self, name: str, out_subset: str, rules_list: [str]):
        membership_degrees = []

        for rule in rules_list:
            set_name: str = rule.split(".")[0]
            subset_name: str = rule.split(".")[-1]

            membership_degrees.append(
                self.get_subset(set_name, subset_name).membership_degree
            )

        for subset in self.out_fuzzy_set.subsets:
            if subset.name == out_subset:
                membership_degrees.append(subset.membership_degree)

        self.rules.append(
            FuzzyRule(name, out_subset, self.get_recursive_fmin(membership_degrees))
        )

        return self

    def get_subset(self, set_name: str, subset_name: str) -> FuzzySubset:
        for fuzzy_set in self.fuzzy_sets:
            if fuzzy_set.name == set_name:
                for subset in fuzzy_set.subsets:
                    if subset.name == subset_name:
                        return subset

        raise Exception("No subset found")

    def get_recursive_fmin(self, values: []):
        if len(values) < 2:
            raise Exception(f"At least 2 values are needed, only {len(values)} found")

        x2 = values.pop()

        if len(values) == 1:
            x1 = values[0]
        else:
            x1 = self.get_recursive_fmin(values)

        return np.fmin(x1, x2)

    def get_recursive_fmax(self, values: []):
        if len(values) < 2:
            raise Exception(f"At least 2 values are needed, only {len(values)} found")

        x2 = values.pop()

        if len(values) == 1:
            x1 = values[0]
        else:
            x1 = self.get_recursive_fmax(values)

        return np.fmax(x1, x2)

    def defuzzify(self, defuzzification_method: str):
        rule_results = []

        # get rules for each output subset
        for out_subset in self.out_fuzzy_set.subsets:
            subset_rules_minima = []

            for rule in self.rules:
                if rule.out_subset == out_subset.name:
                    subset_rules_minima.append(rule.minima)

            if len(subset_rules_minima) > 1:
                rule_results.append(
                    self.get_recursive_fmax(subset_rules_minima)
                )

        # run recursive fmax function for each of them
        out_margin = self.get_recursive_fmax(rule_results)

        # defuzzify the result
        defuzzified = fuzz.defuzz(self.out_fuzzy_set.x_range, out_margin, defuzzification_method)
        result = fuzz.interp_membership(self.out_fuzzy_set.x_range, out_margin, defuzzified)

        # plot output diagram
        plot_output(
            out_set=self.out_fuzzy_set,
            out_margin=out_margin,
            defuzzified=defuzzified,
            result=result
        )

        return defuzzified

    def plot_sets(self):
        for fuzzy_set in self.fuzzy_sets:
            fuzzy_set.plot()

        self.out_fuzzy_set.plot()
