# Value-Based pricing suggestions for SaaS products using Fuzzy Logic

In this project we have built a Mamdani style Fuzzy Inference System (FIS) that takes as an input a number of environmental crisp parameters of a Software as a Service (SaaS) product which and returns a suggested profit margin that can be any value for 10% to 300%. We chose the Mamdani type of system because its intuitiveness, suitability for human input and easily interpretable rule base was suitable for the approach we took to solve the problem.

## Getting started

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. You can now change up the input variables in `main.py` to run the FIS.

## Structure

The system follows a MISO (Multi Input Single Output) structure, consists of X rule bases and is composed of three main modules, fuzzification, inference and defuzzification. The input fuzzy sets and rules are generated using common sense by experienced field experts so the system is built with modularity and readability in mind so changing the parameters or rules can be as easy as possible.

### Fuzzy Sets

Listed below are all the fuzzy sets that we use in our system. For our purposes we used only `trapezoidal` and `triangular` membership functions to represent each of the subsets.

* Pricing term (short, mid, long)
* Monthly active users (low, mid, high)
* Daily usage hours (low, mid, high)
* Monthly net positive feedback (negative, low, mid, high)
* Product market GDP (low, mid, high)
* ...

### Fuzzification

During this process the crisp inputs are taken and fuzzified, so we can get their membership degree and linguistic qualifier.

#### Rules

Our rule base is made of X rules and all of them are encoded in a human-readable manner. When adding a rule we need to specify its name, the subset of the output fuzzy set and also a rules list. The rules list is composed by a list of strings which each one of the strings represents a subset of one of the input fuzzy sets that satisfies the rule. the format of the string is as follows: `[set_name].[subset_name]`. The rule declarations are all documented inside a [Google Sheet](https://docs.google.com/spreadsheets/d/189TuTApM-iDm14cHHxfbSh8yGliFTGe7V4G-6Hky6bg/edit?usp=sharing) document. 

### Inference

During the inference the minima value is calculated for each one of the declared rules by executing a recursive `numpy.fmin(...)` function between all the membership degrees of the fuzzy sets that take part in that rule.

### Defuzzification

During the defuzzification process we get all the minima values for each output subset and again for each subset we execute a recursive `numpy.fmax(...)` function in order to get the output margin area of the output fuzzy set. After we have the area we run a `centroid` defuzzification method to get the final output crisp value.

## Future work

Currently, the system is validated by human reasoning but in the future a testing module could be added. By extracting the crisp inputs from public SaaS companies and comparing the generated result from the system with their actual profit margins we can get an idea of how close the suggested profit margins are to the real world. If the validation module proves to be plausible, a way of optimizing the system can be running a genetic algorithm to generate the best possible rule set and/or membership functions.

## Experts

John Doe - john.doe@gmail.com\
John Doe - john.doe@gmail.com

## Collaborators

Frencis Balla - s371513@oslomet.no\
Jackson Herbert Sinamenye - s371140@oslomet.no\
Kelechukwu Innocent Ede - s371511@oslomet.no
