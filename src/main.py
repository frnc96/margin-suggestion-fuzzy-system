import time
from src.fuzzy.InferenceSystem import FuzzyInferenceSystem as Fis

exec_start_time = time.time()

# Inputs--------------------#
basePrice_usd = 49.99       #
pricingTerm_months = 24     #
companyFocus_val = 180      #
# Inputs--------------------#

fuzzyInferenceSystem = Fis()

# Pricing term fuzzy set and membership functions
pricingTerm_setName = "pricing_term"
fuzzyInferenceSystem\
    .add_set(name=pricingTerm_setName, x_min=100, x_max=251, x=pricingTerm_months)\
    .add_subset(name="short", set_name=pricingTerm_setName, membership_range=[-30, -5, 180, 200])\
    .add_subset(name="mid", set_name=pricingTerm_setName, membership_range=[180, 200, 220, 240])\
    .add_subset(name="long", set_name=pricingTerm_setName, membership_range=[220, 240, 250, 270])

# Company focus fuzzy set and membership functions
companyFocus_setName = "company_focus"
fuzzyInferenceSystem\
    .add_set(name=companyFocus_setName, x_min=100, x_max=251, x=companyFocus_val)\
    .add_subset(name="development", set_name=companyFocus_setName, membership_range=[-30, -5, 180, 200])\
    .add_subset(name="maintenance", set_name=companyFocus_setName, membership_range=[180, 200, 220, 240])\
    .add_subset(name="profits", set_name=companyFocus_setName, membership_range=[220, 240, 250, 270])

# Company focus fuzzy set and membership functions
fuzzyInferenceSystem\
    .add_out_set(name="output_margin", x_min=0, x_max=46)\
    .add_out_subset(name="slim", membership_range=[0, 0, 5, 10])\
    .add_out_subset(name="little", membership_range=[5, 10, 15, 20])\
    .add_out_subset(name="mid", membership_range=[15, 20, 25, 30])\
    .add_out_subset(name="high", membership_range=[25, 30, 35, 40])\
    .add_out_subset(name="very_high", membership_range=[35, 40, 45, 50])

# Rule base
fuzzyInferenceSystem\
    .add_rule(name="Rule#1", out_subset="mid", rules_list=["pricing_term.short"])\
    .add_rule(name="Rule#2", out_subset="little", rules_list=["pricing_term.mid"])\
    .add_rule(name="Rule#3", out_subset="slim", rules_list=["pricing_term.long"])\
    .add_rule(name="Rule#4", out_subset="slim", rules_list=["company_focus.development"])\
    .add_rule(name="Rule#5", out_subset="little", rules_list=["company_focus.maintenance"])\
    .add_rule(name="Rule#6", out_subset="mid", rules_list=["company_focus.profits"])
    # .add_rule(name="Rule#7", out_subset="high", rules_list=["company_focus.maintenance", "pricing_term.mid"])\
    # .add_rule(name="Rule#8", out_subset="high", rules_list=["company_focus.maintenance", "pricing_term.mid"])\
    # .add_rule(name="Rule#9", out_subset="very_high", rules_list=["company_focus.profits", "pricing_term.short"])\
    # .add_rule(name="Rule#10", out_subset="very_high", rules_list=["company_focus.profits", "pricing_term.short"])

outputValue_crisp = fuzzyInferenceSystem.defuzzify(defuzzification_method='centroid')

print(f"Base Price: ${basePrice_usd}")
print(f"Profit margin: %{(outputValue_crisp * 100):.3f}")
print(f"Suggested Price: ${(basePrice_usd + (basePrice_usd * outputValue_crisp)):.3f}")

# Script execution info
print(f'\nScript executed in {(time.time() - exec_start_time):.3f} seconds')
