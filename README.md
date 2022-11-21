# Value-Based pricing suggestions for SaaS products using Fuzzy Logic

Problem description...

### Getting started

1. Clone the repository
2. Install the dependencies with `pip install -r requirements.txt`
3. You can now change code in `main.py` to run the project with different parameters.

### Structure

* Fuzzification
  * Crisp Inputs
    * Cost Amount (cost of maintaining the product)
  * Fuzzy Input Sets
    * Pricing term (short, mid, long)
    * Monthly active users (low, mid, high)
    * Daily usage hours (low, mid, high)
    * Monthly net positive feedback (negative, low, mid, high)
    * Product market GDP (low, mid, high)
  * Fuzzy Rules
    * [Rule-set Google Sheet](https://docs.google.com/spreadsheets/d/189TuTApM-iDm14cHHxfbSh8yGliFTGe7V4G-6Hky6bg/edit?usp=sharing)
* Inference
* Defuzzification
  * Crisp value of profit margin
  * Final price while taking in consideration the base price
* Testing
  * Verify generated profit margin with that of a famous Sass product

## Collaborators

Frencis Balla - s371513@oslomet.no\
Jackson Herbert Sinamenye - s371140@oslomet.no\
Kelechukwu Innocent Ede - s371511@oslomet.no
