import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf
from src.fuzzy.Set import FuzzySet
from src.fuzzy.Rule import FuzzyRule
from src.fuzzy.Subset import FuzzySubset


class FuzzyInferenceSystem:
    def __init__(self):
        self.fuzzy_sets: [FuzzySet] = []
        self.rules: [FuzzyRule] = []
        self.out_fuzzy_set = None

    def add_set(self, name: str, x_min: int, x_max: int, x: int):
        self.fuzzy_sets.append(
            FuzzySet(name, x_min, x_max, x)
        )

        return self

    def add_out_set(self, name: str, x_min: int, x_max: int):
        self.out_fuzzy_set = FuzzySet(name, x_min, x_max)

        return self

    # todo - experiment with other shapes other than trapezoid
    def add_subset(self, name: str, set_name: str, membership_range: [float]):
        for fuzzy_set in self.fuzzy_sets:
            if fuzzy_set.name == set_name:
                membership_degree = fuzz.interp_membership(
                    fuzzy_set.x_range,
                    mf.trapmf(fuzzy_set.x_range, membership_range),
                    fuzzy_set.x
                )
                fuzzy_set.add_subset(
                    FuzzySubset(name, membership_degree)
                )
                break

        return self

    # todo - experiment with other shapes other than trapezoid
    def add_out_subset(self, name: str, membership_range: [float]):
        self.out_fuzzy_set.add_subset(
            FuzzySubset(
                name=name,
                membership_degree=mf.trapmf(self.out_fuzzy_set.x_range, membership_range)
            )
        )

        return self

    def add_rule(self, name: str, out_subset: str, rules_list: []):
        membership_degrees = []

        for rule in rules_list:
            set_name = rule.split(".")[0]
            subset_name = rule.split(".")[-1]

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

    def get_recursive_fmin(self, values: []):
        x2 = values.pop()

        if len(values) == 1:
            x1 = values[0]
        else:
            x1 = self.get_recursive_fmin(values)

        return np.fmin(x1, x2)

    def get_recursive_fmax(self, values: []):
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

        # Defuzzify the result
        defuzzified = fuzz.defuzz(self.out_fuzzy_set.x_range, out_margin, defuzzification_method)

        return fuzz.interp_membership(self.out_fuzzy_set.x_range, out_margin, defuzzified)
