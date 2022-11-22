from src.fuzzy.InferenceSystem import FuzzyInferenceSystem as Fis

# Inputs--------------------------------------------------------------------------------------------------------------#
basePrice_usd = 49.99                                                                                                 #
pricingTerm_months = 10                                                                                               #
productRating_stars = 5                                                                                               #
# Inputs--------------------------------------------------------------------------------------------------------------#

# Initialization of the Fuzzy Inference System
fuzzyInferenceSystem = Fis()

# Here we declare all the input fuzzy sets and their membership functions
pricingTerm_setName = "pricing_term"
fuzzyInferenceSystem\
    .add_set(name=pricingTerm_setName, x_min=1, x_max=12, step=1, x=pricingTerm_months)\
    .add_subset(name="short", set_name=pricingTerm_setName, membership_range=[-30, -5, 2, 4], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=pricingTerm_setName, membership_range=[2, 4, 6, 8], mf_type="trapezoidal")\
    .add_subset(name="long", set_name=pricingTerm_setName, membership_range=[6, 8, 17, 30], mf_type="trapezoidal")

productRating_setName = "product_rating"
fuzzyInferenceSystem\
    .add_set(name=productRating_setName, x_min=1, x_max=5, step=0.25, x=productRating_stars)\
    .add_subset(name="low", set_name=productRating_setName, membership_range=[-20, -20, 2.75, 3.25], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=productRating_setName, membership_range=[2.75, 3.5, 4.25], mf_type="triangular")\
    .add_subset(name="high", set_name=productRating_setName, membership_range=[3.75, 4.25, 20, 20], mf_type="trapezoidal")

# Here we declare the output fuzzy set which is the profit margin suggestion. We set a minimum margin of 10% and a
# maximum margin of 300%, we also map the five trapezoidal shaped subsets accordingly.
fuzzyInferenceSystem\
    .add_out_set(name="output_margin", x_min=0, x_max=3, step=0.01)\
    .add_out_subset(name="slim", membership_range=[-20, -20, 0.1, 0.25], mf_type="trapezoidal")\
    .add_out_subset(name="little", membership_range=[0.1, 0.35, 0.7], mf_type="triangular")\
    .add_out_subset(name="mid", membership_range=[0.4, 0.9, 1.4], mf_type="triangular")\
    .add_out_subset(name="high", membership_range=[1, 1.62, 2.25], mf_type="triangular")\
    .add_out_subset(name="very_high", membership_range=[1.75, 2.25, 20, 20], mf_type="trapezoidal")

# Plot the sets
fuzzyInferenceSystem.plot_sets()

# Here we define the rule base, each rule has a name for identification and the corresponding output subset. The rule
# list stores all the input subsets that lead to that output subset. That list is populated by strings that are composed
# by the name of the fuzzy set, and it's subset separated by a dot character. This way the list of rules is readable.
fuzzyInferenceSystem\
    .add_rule(name="Rule#1", out_subset="mid", rules_list=["pricing_term.short"])\
    .add_rule(name="Rule#2", out_subset="little", rules_list=["pricing_term.mid"])\
    .add_rule(name="Rule#3", out_subset="slim", rules_list=["pricing_term.long"])\
    .add_rule(name="Rule#4", out_subset="slim", rules_list=["product_rating.low"])\
    .add_rule(name="Rule#5", out_subset="little", rules_list=["product_rating.mid"])\
    .add_rule(name="Rule#6", out_subset="mid", rules_list=["product_rating.high"])

# Run a centroid defuzzification method to get a crisp output
outputValue_crisp = fuzzyInferenceSystem.defuzzify(defuzzification_method='centroid')

# Print out the results
print(f"Base Price: ${basePrice_usd}")
print(f"Profit margin: %{(outputValue_crisp * 100):.3f}")
print(f"Suggested Price: ${(basePrice_usd + (basePrice_usd * outputValue_crisp)):.3f}")
