from dataclasses import dataclass


@dataclass
class FuzzySubset:
    name: str
    membership_degree: [float]
    membership_range: [float]
