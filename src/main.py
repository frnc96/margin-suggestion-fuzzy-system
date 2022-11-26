from src.fuzzy.InferenceSystem import FuzzyInferenceSystem as Fis

# Inputs--------------------------------------------------------------------------------------------------------------#
basePrice_usd = 50
productLifetime_years = 10
monthlyActive_users = 10
thirdParty_integrations = 3
enterprise_features = 3
branding_usd = 100
targetAudienceMeanIncome_usd = 50000
# Inputs--------------------------------------------------------------------------------------------------------------#

# Initialization of the Fuzzy Inference System
fuzzyInferenceSystem = Fis()

# Here we declare all the input fuzzy sets and their membership functions (MF)
# MF types can be 'trapezoidal' or 'triangular'
# todo - set ranges
set1_name = "product_lifetime"
fuzzyInferenceSystem\
    .add_set(name=set1_name, x_min=1, x_max=10, step=1, x=productLifetime_years)\
    .add_subset(name="early", set_name=set1_name, membership_range=[-30, -5, 2, 4], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set1_name, membership_range=[2, 4, 6, 8], mf_type="trapezoidal")\
    .add_subset(name="mature", set_name=set1_name, membership_range=[6, 8, 17, 30], mf_type="trapezoidal")

# todo - set ranges
set2_name = "monthly_active_users"
fuzzyInferenceSystem\
    .add_set(name=set2_name, x_min=1, x_max=10, step=1, x=monthlyActive_users)\
    .add_subset(name="low", set_name=set2_name, membership_range=[-30, -5, 2, 4], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set2_name, membership_range=[2, 4, 6, 8], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set2_name, membership_range=[6, 8, 17, 30], mf_type="trapezoidal")

# todo - set ranges
set3_name = "third_party_integrations"
fuzzyInferenceSystem\
    .add_set(name=set3_name, x_min=1, x_max=10, step=1, x=thirdParty_integrations)\
    .add_subset(name="low", set_name=set3_name, membership_range=[-30, -5, 2, 4], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set3_name, membership_range=[2, 4, 6, 8], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set3_name, membership_range=[6, 8, 17, 30], mf_type="trapezoidal")

# todo - set ranges
set4_name = "enterprise_features"
fuzzyInferenceSystem\
    .add_set(name=set4_name, x_min=1, x_max=10, step=1, x=enterprise_features)\
    .add_subset(name="low", set_name=set4_name, membership_range=[-30, -5, 2, 4], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set4_name, membership_range=[2, 4, 6, 8], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set4_name, membership_range=[6, 8, 17, 30], mf_type="trapezoidal")

# todo - set ranges
set5_name = "branding"
fuzzyInferenceSystem\
    .add_set(name=set5_name, x_min=1, x_max=10, step=1, x=branding_usd)\
    .add_subset(name="budget", set_name=set5_name, membership_range=[-30, -5, 2, 4], mf_type="trapezoidal")\
    .add_subset(name="value", set_name=set5_name, membership_range=[2, 4, 6, 8], mf_type="trapezoidal")\
    .add_subset(name="premium", set_name=set5_name, membership_range=[6, 8, 17, 30], mf_type="trapezoidal")

# todo - set ranges
set7_name = "target_audience_mean_income"
fuzzyInferenceSystem\
    .add_set(name=set7_name, x_min=1, x_max=10, step=1, x=targetAudienceMeanIncome_usd)\
    .add_subset(name="low", set_name=set7_name, membership_range=[-30, -5, 2, 4], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set7_name, membership_range=[2, 4, 6, 8], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set7_name, membership_range=[6, 8, 17, 30], mf_type="trapezoidal")


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
rule_list = [
    ["Rule#1", "little",    ["product_lifetime.early"]],
    ["Rule#2", "slim",      ["product_lifetime.early", "branding.budget"]],
    ["Rule#3", "slim",      ["product_lifetime.early", "target_audience_mean_income.low"]],
    ["Rule#4", "little",    ["product_lifetime.early", "branding.value", "target_audience_mean_income.mid"]],
    ["Rule#5", "mid",       ["product_lifetime.early", "branding.premium", "target_audience_mean_income.high"]],
    ["Rule#6", "little",    ["product_lifetime.mid", "monthly_active_users.low"]],
]
for rule_item in rule_list:
    fuzzyInferenceSystem.add_rule(name=rule_item[0], out_subset=rule_item[1], rules_list=rule_item[2])

# Run a centroid defuzzification method to get a crisp output. Other methods can be:
# 'bisector': bisector of area
# 'mom' : mean of maximum
# 'som' : min of maximum
# 'lom' : max of maximum
outputValue_crisp = fuzzyInferenceSystem.defuzzify(defuzzification_method='centroid')

# Print out the results
print(f"Base Price: ${basePrice_usd}/month")
print(f"Profit margin: %{outputValue_crisp * 100}")
print(f"Suggested Price: ${(basePrice_usd + (basePrice_usd * outputValue_crisp)):.2f}/month")
