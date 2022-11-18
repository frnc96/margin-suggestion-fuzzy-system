from dataclasses import dataclass


@dataclass
class FuzzyRule:
    name: str
    out_subset: str
    minima: [float]
