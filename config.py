from datetime import date

expiry_date = date(2025, 10, 1)  # Year, Month, Day

opening_year = date.today().year
explanations = "yes"  # this is somewhat historical. At the moment, nothing changes on this. However, there are some items in viz_widgets that are conditional on this being 'yes'. Eventually I'll update viz_widgets to clean this up and make this variable redundant.

individual_or_couple = "couple"
client1_gender = "male"
client1_name = "Jack"
client1_age = 39
client2_name = "Jill"
client2_age = 37
client_to_benchmark = client1_name
benchmark_age = client1_age
age_to_follow_to = 100
years_to_model = age_to_follow_to - benchmark_age
client1_retirement_age = 65
client2_retirement_age = 65
opening_investment_balance = 200000
nz_super_age_eligibility = 65
nz_super_couple_both = 39700
nz_super_couple_one_of_two = 19800
nz_super_individual = 25800
investment_threshold = 100000
investment_returns_under_threshold = 0
investment_returns_over_threshold = 0.04
investment_probabilistic_approach_yes_or_no = "no"
investment_probabilistic_methodology = "normal"  # Original value
investment_probabilistic_methodology_normal_sd_multiplier = 1  # Original value
investment_probabilistic_number_of_scenarios = 20  # Original value
retirement_expenditure_couple = 70000
retirement_expenditure_individual = 50000
age_retirement_expenditure_starts_reducing = 80
retirement_expenditure_annual_reduction = 0.03
retirement_expenditure_minimum_couple = 50000
retirement_expenditure_minimum_individual = 40000
current_savings_rate = 15000
savings_rate_change_age = 55
updated_savings_rate = 25000
savings_rate_change2_age = 60  # Original value
updated_savings_rate2 = current_savings_rate  # Original value
post_retirement_earned_income = 0  # Original value
post_retirement_years_of_earned_income = 5  # Original value
age_when_one_passes_away = 100  # Original value
periodic_expenditure = 25000
age_periodic_expenditure_begins = 40  # Original value
periodic_expenditure_frequency = 5
age_periodic_expenditure_ends = 75
one_off_item_purchase_price = 0  # Original value
age_one_off_item_purchased = 0  # Original value
one_off_item_ongoing_costs = 0  # Original value
age_one_off_item_sold = 0  # Original value
one_off_item_sale_price = one_off_item_purchase_price  # Original value
providing_substantial_assistance_to_children_yes_or_no = "no"
children_yes_or_no = "yes"
number_of_children = 1
child1_age = client1_age - 28
child2_age = client1_age - 30
child3_age = client1_age - 32
child4_age = client1_age - 34
child5_age = client1_age - 36
assisting_with_education_for_children_yes_or_no = (
    "yes"  # redundant, need to keep as "yes" until I update other modules
)
annual_amount_of_educational_assistance = 0
age_of_providing_initial_educational_assistance = 19
years_of_providing_educational_assistance = 5
education_start_year_child1 = (
    age_of_providing_initial_educational_assistance - child1_age
)
education_start_year_child2 = (
    age_of_providing_initial_educational_assistance - child2_age
)
education_start_year_child3 = (
    age_of_providing_initial_educational_assistance - child3_age
)
education_start_year_child4 = (
    age_of_providing_initial_educational_assistance - child4_age
)
education_start_year_child5 = (
    age_of_providing_initial_educational_assistance - child5_age
)
education_end_year_child1 = (
    education_start_year_child1 + years_of_providing_educational_assistance
)
education_end_year_child2 = (
    education_start_year_child2 + years_of_providing_educational_assistance
)
education_end_year_child3 = (
    education_start_year_child3 + years_of_providing_educational_assistance
)
education_end_year_child4 = (
    education_start_year_child4 + years_of_providing_educational_assistance
)
education_end_year_child5 = (
    education_start_year_child5 + years_of_providing_educational_assistance
)
providing_one_off_assistance_to_children_yes_or_no = (
    "yes"  # redundant, need to keep as "yes" until I update other modules
)
amount_of_one_off_assistance_to_children = 0
age_of_one_off_assistance_to_children = 28
allow_for_one_off_items_yes_or_no = "no"
one_off_item1 = 0
one_off_item2 = 0
one_off_item3 = 0
one_off_item4 = 0
one_off_item5 = 0
one_off_item1_age = 50
one_off_item2_age = 55
one_off_item3_age = 60
one_off_item4_age = 65
one_off_item5_age = 70
