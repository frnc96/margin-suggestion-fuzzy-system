from src.fuzzy.InferenceSystem import FuzzyInferenceSystem as Fis

# Inputs--------------------------------------------------------------------------------------------------------------#
basePrice_usd = 50                       # Base price of the products
productLifetime_years = 7                # How long has the product bee on the market
monthlyActive_kUsers = 75                # How many monthly active users use the product
thirdParty_integrations = 3              # How many third party integrations does the product offer
enterprise_features = 1                  # How many enterprise features does the product offer
branding_percent = 5                     # What percentage of revenue is spent on marketing
targetAudienceMeanIncome_kUsd = 110      # Mean income of the targeted audience
# Inputs--------------------------------------------------------------------------------------------------------------#

# Initialization of the Fuzzy Inference System
fuzzyInferenceSystem = Fis()

# Here we declare all the input fuzzy sets and their membership functions (MF)
# MF types can be 'trapezoidal' or 'triangular'
set1_name = "product_lifetime"
fuzzyInferenceSystem\
    .add_set(name=set1_name, x_min=0, x_max=10, step=.5, x=productLifetime_years)\
    .add_subset(name="early", set_name=set1_name, membership_range=[0, 0, 1.5, 5], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set1_name, membership_range=[3, 5.5, 8], mf_type="triangular")\
    .add_subset(name="mature", set_name=set1_name, membership_range=[5.5, 8, 10, 10], mf_type="trapezoidal")

set2_name = "monthly_active_users"
fuzzyInferenceSystem\
    .add_set(name=set2_name, x_min=0, x_max=100, step=.001, x=monthlyActive_kUsers)\
    .add_subset(name="low", set_name=set2_name, membership_range=[0, 0, 10], mf_type="triangular")\
    .add_subset(name="mid", set_name=set2_name, membership_range=[5, 20, 50, 65], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set2_name, membership_range=[40, 60, 100, 100], mf_type="trapezoidal")

set3_name = "third_party_integrations"
fuzzyInferenceSystem\
    .add_set(name=set3_name, x_min=0, x_max=100, step=1, x=thirdParty_integrations)\
    .add_subset(name="low", set_name=set3_name, membership_range=[0, 0, 10, 20], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set3_name, membership_range=[10, 25, 45, 70], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set3_name, membership_range=[40, 60, 100, 100], mf_type="trapezoidal")

set4_name = "enterprise_features"
fuzzyInferenceSystem\
    .add_set(name=set4_name, x_min=0, x_max=10, step=1, x=enterprise_features)\
    .add_subset(name="low", set_name=set4_name, membership_range=[0, 0, 2], mf_type="triangular")\
    .add_subset(name="mid", set_name=set4_name, membership_range=[1, 2, 5, 6], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set4_name, membership_range=[5, 6, 10, 10], mf_type="trapezoidal")

set5_name = "branding"
fuzzyInferenceSystem\
    .add_set(name=set5_name, x_min=0, x_max=100, step=.1, x=branding_percent)\
    .add_subset(name="budget", set_name=set5_name, membership_range=[0, 0, 10, 30], mf_type="trapezoidal")\
    .add_subset(name="value", set_name=set5_name, membership_range=[20, 30, 50, 70], mf_type="trapezoidal")\
    .add_subset(name="premium", set_name=set5_name, membership_range=[50, 65, 100, 100], mf_type="trapezoidal")

set7_name = "target_audience_mean_income"
fuzzyInferenceSystem\
    .add_set(name=set7_name, x_min=0, x_max=300, step=1, x=targetAudienceMeanIncome_kUsd)\
    .add_subset(name="low", set_name=set7_name, membership_range=[0, 0, 10, 45], mf_type="trapezoidal")\
    .add_subset(name="mid", set_name=set7_name, membership_range=[25, 60, 120, 180], mf_type="trapezoidal")\
    .add_subset(name="high", set_name=set7_name, membership_range=[110, 190, 300, 300], mf_type="trapezoidal")


# Here we declare the output fuzzy set which is the profit margin suggestion. We set a minimum margin of 10% and a
# maximum margin of 300%, we also map the five trapezoidal shaped subsets accordingly.
fuzzyInferenceSystem\
    .add_out_set(name="output_margin", x_min=0, x_max=3, step=0.01)\
    .add_out_subset(name="slim", membership_range=[0, 0, 0.1, 0.25], mf_type="trapezoidal")\
    .add_out_subset(name="little", membership_range=[0.1, 0.25, 0.45, 0.7], mf_type="trapezoidal")\
    .add_out_subset(name="mid", membership_range=[0.4, 0.7, 1.1, 1.4], mf_type="trapezoidal")\
    .add_out_subset(name="high", membership_range=[1, 1.42, 1.82, 2.25], mf_type="trapezoidal")\
    .add_out_subset(name="very_high", membership_range=[1.75, 2.25, 3, 3], mf_type="trapezoidal")

# Plot the sets
fuzzyInferenceSystem.plot_sets()

# Here we define the rule base, each rule has a name for identification and the corresponding output subset. The rule
# list stores all the input subsets that lead to that output subset. That list is populated by strings that are composed
# by the name of the fuzzy set, and it's subset separated by a dot character. This way the list of rules is readable.
rule_list = [
    ["Rule#1", "little",        ["product_lifetime.early"]],
    ["Rule#2", "slim",          ["product_lifetime.early", "branding.budget"]],
    ["Rule#3", "slim",          ["product_lifetime.early", "target_audience_mean_income.low"]],
    ["Rule#4", "little",        ["product_lifetime.early", "branding.value", "target_audience_mean_income.mid"]],
    ["Rule#5", "mid",           ["product_lifetime.early", "branding.premium", "target_audience_mean_income.high"]],
    ["Rule#6", "little",        ["product_lifetime.mid", "monthly_active_users.low"]],
    ["Rule#7", "little",        ["product_lifetime.mid", "third_party_integrations.low"]],
    ["Rule#8", "little",        ["product_lifetime.mid", "branding.value"]],
    ["Rule#9", "mid",           ["product_lifetime.mid", "target_audience_mean_income.mid"]],
    ["Rule#10", "high",         ["product_lifetime.mid", "target_audience_mean_income.high"]],
    ["Rule#11", "high",         ["product_lifetime.mid", "monthly_active_users.mid", "target_audience_mean_income.mid"]],
    ["Rule#12", "mid",          ["product_lifetime.mid", "enterprise_features.mid"]],
    ["Rule#13", "high",         ["product_lifetime.mid", "enterprise_features.high"]],
    ["Rule#14", "very_high",    ["product_lifetime.mid", "enterprise_features.high", "branding.premium"]],
    ["Rule#15", "high",         ["product_lifetime.mid", "monthly_active_users.high", "third_party_integrations.high"]],
    ["Rule#16", "mid",          ["product_lifetime.mid", "third_party_integrations.mid", "enterprise_features.low"]],
    ["Rule#17", "mid",          ["product_lifetime.mid", "branding.budget", "target_audience_mean_income.high"]],
    ["Rule#18", "little",       ["product_lifetime.mature", "monthly_active_users.low", "third_party_integrations.low", "enterprise_features.low"]],
    ["Rule#19", "high",         ["product_lifetime.mature", "monthly_active_users.high", "enterprise_features.high"]],
    ["Rule#20", "very_high",    ["product_lifetime.mature", "monthly_active_users.high", "third_party_integrations.high", "enterprise_features.high"]],
    ["Rule#21", "high",         ["product_lifetime.mature", "branding.premium", "target_audience_mean_income.high"]],
    ["Rule#22", "mid",          ["product_lifetime.mature", "branding.value", "target_audience_mean_income.mid"]],
    ["Rule#23", "mid",          ["product_lifetime.mature", "third_party_integrations.mid", "target_audience_mean_income.low"]],
    ["Rule#24", "mid",          ["product_lifetime.mature", "monthly_active_users.mid", "third_party_integrations.high"]],
    ["Rule#25", "high",         ["product_lifetime.mature", "enterprise_features.mid", "branding.premium"]],
    ["Rule#26", "high",         ["monthly_active_users.high", "third_party_integrations.high", "enterprise_features.high"]],
    ["Rule#27", "very_high",    ["monthly_active_users.high", "third_party_integrations.high", "enterprise_features.high", "branding.premium", "target_audience_mean_income.high"]],
    ["Rule#28", "little",       ["monthly_active_users.low", "third_party_integrations.low", "enterprise_features.low", "branding.budget"]],
    ["Rule#29", "mid",          ["monthly_active_users.mid", "third_party_integrations.mid", "enterprise_features.mid"]],
    ["Rule#30", "mid",          ["branding.value", "target_audience_mean_income.mid"]],
    ["Rule#31", "slim",         ["monthly_active_users.low", "third_party_integrations.low", "enterprise_features.low", "branding.budget", "target_audience_mean_income.low"]],
    ["Rule#32", "high",         ["third_party_integrations.low", "enterprise_features.low", "branding.premium", "target_audience_mean_income.high"]],
]

# All the rules are inserted into the FIS
for rule_item in rule_list:
    fuzzyInferenceSystem.add_rule(name=rule_item[0], out_subset=rule_item[1], rules_list=rule_item[2])

# Run a centroid defuzzification method to get a crisp output. Other methods can be:
# 'bisector': bisector of area
# 'mom' : mean of maximum
# 'som' : min of maximum
# 'lom' : max of maximum
outputValue_crisp = fuzzyInferenceSystem.defuzzify(defuzzification_method='centroid')

# Print out the results
print(f"Base Price: ${basePrice_usd}")
print(f"Profit margin: %{outputValue_crisp * 100}")
print(f"Suggested Price: ${(basePrice_usd + (basePrice_usd * outputValue_crisp)):.2f}")
