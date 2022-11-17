import time
import numpy as np
import skfuzzy as fuzz
import skfuzzy.membership as mf
import matplotlib.pyplot as plt

exec_start_time = time.time()

# Inputs--------------------#
basePrice_usd = 49.99       #
pricingTerm_months = 24     #
companyFocus_val = 180      #
# Inputs--------------------#

# Fuzzy sets
pricingTerm_set = np.arange(100, 251, 1)
companyFocus_set = np.arange(100, 251, 1)
margin_set = np.arange(0, 46, 1)

# Set membership functions
pricingTerm_short = mf.trapmf(pricingTerm_set, [-30, -5, 180, 200])
pricingTerm_mid = mf.trapmf(pricingTerm_set, [180, 200, 220, 240])
pricingTerm_long = mf.trapmf(pricingTerm_set, [220, 240, 250, 270])

companyFocus_development = mf.trapmf(companyFocus_set, [-30, -5, 180, 200])
companyFocus_maintenance = mf.trapmf(companyFocus_set, [180, 200, 220, 240])
companyFocus_profits = mf.trapmf(companyFocus_set, [220, 240, 250, 270])

margin_slim = mf.trapmf(margin_set, [0, 0, 5, 10])
margin_little = mf.trapmf(margin_set, [5, 10, 15, 20])
margin_mid = mf.trapmf(margin_set, [15, 20, 25, 30])
margin_high = mf.trapmf(margin_set, [25, 30, 35, 40])
margin_veryHigh = mf.trapmf(margin_set, [35, 40, 45, 50])

# Get membership degrees
pricingTerm_fit_short = fuzz.interp_membership(pricingTerm_set, pricingTerm_short, pricingTerm_months)
pricingTerm_fit_mid = fuzz.interp_membership(pricingTerm_set, pricingTerm_mid, pricingTerm_months)
pricingTerm_fit_long = fuzz.interp_membership(pricingTerm_set, pricingTerm_long, pricingTerm_months)

companyFocus_fit_development = fuzz.interp_membership(companyFocus_set, companyFocus_development, companyFocus_val)
companyFocus_fit_maintenance = fuzz.interp_membership(companyFocus_set, companyFocus_maintenance, companyFocus_val)
companyFocus_fit_profits = fuzz.interp_membership(companyFocus_set, companyFocus_profits, companyFocus_val)

# Declare rules
rule1 = np.fmin(pricingTerm_fit_short, margin_mid)
rule2 = np.fmin(pricingTerm_fit_mid, margin_little)
rule3 = np.fmin(pricingTerm_fit_long, margin_slim)

rule4 = np.fmin(companyFocus_fit_development, margin_slim)
rule5 = np.fmin(companyFocus_fit_maintenance, margin_slim)
rule6 = np.fmin(companyFocus_fit_profits, margin_slim)

# Get output fuzzy set (Mamdani)
out_slim = np.fmax(rule3, rule6)
out_little = np.fmax(rule2, rule5)
out_mid = np.fmax(rule1, rule4)
# out_high = np.fmax(rule1)
# out_veryHigh = np.fmax(rule1)

# Defuzzify the output
# out_margin = np.fmax(np.fmax(np.fmax(np.fmax(out_slim, out_little), out_mid), out_high), out_veryHigh)
out_margin = np.fmax(np.fmax(out_slim, out_little), out_mid)
defuzzified = fuzz.defuzz(margin_set, out_margin, 'centroid')
result = fuzz.interp_membership(margin_set, out_margin, defuzzified)

print(f"Base Price: ${basePrice_usd}")
print(f"Profit margin: %{(defuzzified * 100):.3f}")
print(f"Suggested Price: ${(basePrice_usd * defuzzified):.3f}")

# Main function catcher
if __name__ == '__main__':
    print(f'\nScript executed in {(time.time() - exec_start_time):.3f} seconds')
