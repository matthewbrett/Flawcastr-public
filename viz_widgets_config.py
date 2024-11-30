import config


section_titles = {
    1: "Opening balance",
    2: "Savings",
    3: "Investment returns",
    4: "Randomness (Monte Carlo)",
    5: "Retirement, etc",
    6: "NZ Super",
    7: "Periodic expenditure",
    8: "One-off items",
    9: "Assistance to children"
}

config_var_list = [
    {"type": "divider"},
    {
        "type": "input",
        "var_name": "opening_investment_balance",
        "label": "Opening investment balance ($)",
        "explanation": "This represents investment assets, EXCLUDING personal or lifestyle assets, such as the family home(s), vehicles, and the like. If you own a business that you will eventually sell, it is usually best to exclude the value of the business and include its eventual sale as one-off items below. If you have a mortgage repayment and want to include principal repayments on the mortgage as part of your savings (below), subtract your mortgage. If you treat savings (below) as being separate from mortgage repayments, ignore your mortgage.",
    },
    {"type": "divider"},
    {
        "type": "input",
        "var_name": "current_savings_rate",
        "label": "Current savings rate ($)",
    },
    {
        "type": "input",
        "var_name": "savings_rate_change_age",
        "label": "Age savings rate changes",
        "explanation": "Savings rate might change due to repayment of the mortgage (which should free up cash flow for investing; only factor this in if you haven't been including principal repayments on your mortgage as savings already) or children becoming independent.",
    },
    {
        "type": "input",
        "var_name": "updated_savings_rate",
        "label": "Updated savings rate after this age",
    },
    {"type": "divider"},
    {
        "type": "input",
        "var_name": "investment_threshold",
        "label": "Investment threshold ($)",
        "explanation": "This adds a small amount of nuance to investment returns. For example, if the investment threshold is 0.05 and the investment returns under threshold is 0.03, then the investment returns will be 0.03 if the investment balance is less than 5% of the opening investment balance, and 0.05 if the investment balance is greater than 5% of the opening investment balance.",
    },
    {
        "type": "input",
        "var_name": "investment_returns_under_threshold",
        "label": "Investment returns under the threshold (adjusted for inflation) (%)",
    },
    {
        "type": "input",
        "var_name": "investment_returns_over_threshold",
        "label": "Investment returns over the threshold (adjusted for inflation) (%)",
    },
    {
        "type": "text",
        "text": "IMPORTANT: INVESTMENT RETURNS SHOULD BE IN REAL TERMS ",
        "explanation": "Ie, investment returns should be adjusted for inflation. If nominal returns are 5%, for instance, and inflation is 2%, then the real return should be listed as 3%. If this adjustment is not made, then projections will be too optimistic.",
    },
    {
        "type": "text",
        "text": "Also: Flawcastr does not consider leverage ",
        "explanation": "DO NOT USE THIS MODEL TO ASSESS WHETHER TO BORROW TO INVEST. Flawcastr currently doesn't factor in the effect of leverage (for good or bad) on investment outcomes. To the extent this tool is useful for people who are considering whether to borrow to invest, it might help the user to inform whether it is necessary for them to do so in order to meet their financial objectives. If a user has a mortgage, for instance, the simplest way to treat this separately from investment assets, and treat mortgage repayments as expenditure. If and when they expect to repay their mortgage, they can then adjust savings levels to reflect their increased cash flow. If a user takes out a mortgage to buy a house and this requires a deposit that comes from investment assets, that would represent a withdrawal from investment assets (or for the amount they have initially saved, and any contributions to this amount to be ignored as savings for the purpose of this model).",
    },
    {"type": "divider"},
    {
        "type": "toggle",
        "var_name": "investment_probabilistic_approach_yes_or_no",
        "label": "Show Monte Carlo scenarios",
        "explanation": "This shows 20 scenarios that are identical to the deterministic (dark black) scenario, with the one exception being that investment returns each year are randomly* generated. More specifically, each of the 20 scenarios assumes that investment returns follow a normal distribution, with the mean and standard deviation for under- and above-threshold returns being the same as what you haveve selected above. So if under-threshold returns are 1%, then the mean and standard deviation for under-threshold returns will be 1%. If above-threshold returns are 4%, then the mean and standard deviation for above-threshold returns will be 4%. Investment returns do not follow a normal distribution. The most important lesson to take out of this is that investment returns are not likely to be constant, and outcomes can vary significantly. (The same is true with all other variables, which is why this is a FLAWcast, not a forecast!",
    },
    {"type": "divider"},
    {
        "type": "input",
        "var_name": "client1_retirement_age",
        "label": "Age of retirement (age of first-listed user)",
    },
    {
        "type": "input",
        "var_name": "retirement_expenditure_couple",
        "label": "Initial retirement expenditure (couple) ($)",
        "conditional_on": lambda: config.individual_or_couple == "couple",
    },
    {
        "type": "input",
        "var_name": "age_when_one_passes_away",
        "explanation": "(Only relevant for couples.) This morbid scenario is to factor in ongoing financial ramifications associated with one person in a couple passing away. For the purpose of this model, it impacts NZ Super levels and also expenditure.",
        "conditional_on": lambda: config.individual_or_couple == "couple",
    },
    {
        "type": "input",
        "var_name": "retirement_expenditure_individual",
        "label": "Retirement expenditure (individual) ($)",
    },
    {
        "type": "input",
        "var_name": "age_retirement_expenditure_starts_reducing",
        "explanation": "At a certain point during retirement, expenditure tends to reduce. As people go through retirement they often has less energy and inclination to spend money they might have spent earlier in their retirement. This variable and the variables below consider the possibility that from a certain point, retirement expenditure will reduce (in real terms) by a certain percentage each year, down to a certain minimum level of expenditure.",
    },
    {
        "type": "input",
        "var_name": "retirement_expenditure_annual_reduction",
        "label": "Reduction in annual retirement expenditure (in real terms) (%)",
    },
    {
        "type": "input",
        "var_name": "retirement_expenditure_minimum_couple",
        "label": "Minimum retirement expenditure - couple ($)",
        "conditional_on": lambda: config.individual_or_couple == "couple",
    },
    {
        "type": "input",
        "var_name": "retirement_expenditure_minimum_individual",
        "label": "Minimum retirement expedniture - individual ($)",
    },
    {"type": "divider"},
    {
        "type": "input",
        "var_name": "nz_super_age_eligibility",
        "label": "NZ Super - age of eligibility",
        "explanation": "At the time of preparing this model, NZ Super is universal. With very limited exceptions, so long as you qualify for NZ Super you get the same amount, regardless of your asset position or other forms of income. There might be some nuances - for instance, for some people, NZ Super income might be taxed at a different level and there might be other benefits. To keep this model simple it assumes that NZ Super will remain the same level (adjusted for inflation) once the user becomes eligible for it.",
    },
    {
        "type": "input",
        "var_name": "nz_super_couple_both",
        "label": "NZ Super - annual amount for a couple where both are eligible ($)",
        "conditional_on": lambda: config.individual_or_couple == "couple",
    },
    {
        "type": "input",
        "var_name": "nz_super_couple_one_of_two",
        "label": "NZ Super - annual amount for a couple where only one is eligible ($)",
        "conditional_on": lambda: config.individual_or_couple == "couple",
    },
    {
        "type": "input",
        "var_name": "nz_super_individual",
        "label": "NZ Super - annual amount for an individual ($)",
    },
    {"type": "divider"},
    {
        "type": "input",
        "var_name": "periodic_expenditure",
        "label": "Periodic expenditure ($)",
        "explanation": "This represents periodic expenditure that might be incurred very few years, such as car purchases, house repairs and renovations, and/or overseas trips. It assumes the money spent on these one-off items will represent reduced savings during that year or will require withdrawing from investment assets. If you are likely to be able to continue investment savings at the same rate then you don't need to factor in these periodic expenditures.",
    },
    {"type": "input", "var_name": "age_periodic_expenditure_begins"},
    {
        "type": "input",
        "var_name": "periodic_expenditure_frequency",
        "label": "Number of years from one set of periodic expenditure to the next",
    },
    {
        "type": "input",
        "var_name": "age_periodic_expenditure_ends",
        "label": "Age periodic expenditure stops being incurred",
    },
    {"type": "divider"},
    {
        "type": "toggle",
        "var_name": "allow_for_one_off_items_yes_or_no",
        "label": "Allow for one-off items?",
        "explanation": "*Put incomings as positive numbers and outgoings as negative numbers.* One-off items below represent items significant incomings or outgoings on specific years. This might include windfalls (such as a business sale or inheritance), capital freed up by downsizing/rightsizing your home (after repaying any debt), or outgoings such as house renovations.",
    },
    {
        "type": "multi_input",
        "var_name1": "one_off_item1_age",
        "label_one_off_item1_age": "One-off item 1 - Age:",
        "var_name2": "one_off_item1",
        "label_one_off_item1": "Amount ($)",
        "conditional_on": lambda: config.allow_for_one_off_items_yes_or_no == "yes",
    },
    {
        "type": "multi_input",
        "var_name1": "one_off_item2_age",
        "label_one_off_item2_age": "One-off item 2 - Age:",
        "var_name2": "one_off_item2",
        "label_one_off_item2": "Amount ($)",
        "conditional_on": lambda: config.allow_for_one_off_items_yes_or_no == "yes",
    },
    {
        "type": "multi_input",
        "var_name1": "one_off_item3_age",
        "label_one_off_item3_age": "One-off item 3 - Age:",
        "var_name2": "one_off_item3",
        "label_one_off_item3": "Amount ($)",
        "conditional_on": lambda: config.allow_for_one_off_items_yes_or_no == "yes",
    },
    {
        "type": "multi_input",
        "var_name1": "one_off_item4_age",
        "label_one_off_item4_age": "One-off item 4 - Age:",
        "var_name2": "one_off_item4",
        "label_one_off_item4": "Amount ($)",
        "conditional_on": lambda: config.allow_for_one_off_items_yes_or_no == "yes",
    },
    {
        "type": "multi_input",
        "var_name1": "one_off_item5_age",
        "label_one_off_item5_age": "One-off item 5 - Age:",
        "var_name2": "one_off_item5",
        "label_one_off_item5": "Amount ($)",
        "conditional_on": lambda: config.allow_for_one_off_items_yes_or_no == "yes",
    },

    {"type": "divider"},
    {
        "type": "toggle",
        "var_name": "providing_substantial_assistance_to_children_yes_or_no",
        "label": "Provide for substantial assistance to children?",
    },
    {
        "type": "input",
        "var_name": "number_of_children",
        "conditional_on": lambda: config.providing_substantial_assistance_to_children_yes_or_no
        == "yes",
    },
    {
        "type": "input",
        "var_name": "child1_age",
        "conditional_on": lambda: config.number_of_children >= 1
        and config.providing_substantial_assistance_to_children_yes_or_no == "yes",
        "label": "Age of first child",
    },
    {
        "type": "input",
        "var_name": "child2_age",
        "conditional_on": lambda: config.number_of_children >= 2
        and config.providing_substantial_assistance_to_children_yes_or_no == "yes",
        "label": "Age of second child",
    },
    {
        "type": "input",
        "var_name": "child3_age",
        "conditional_on": lambda: config.number_of_children >= 3
        and config.providing_substantial_assistance_to_children_yes_or_no == "yes",
        "label": "Age of third child",
    },
    {
        "type": "input",
        "var_name": "child4_age",
        "conditional_on": lambda: config.number_of_children >= 4
        and config.providing_substantial_assistance_to_children_yes_or_no == "yes",
        "label": "Age of fourth child",
    },
    {
        "type": "input",
        "var_name": "child5_age",
        "conditional_on": lambda: config.number_of_children >= 5
        and config.providing_substantial_assistance_to_children_yes_or_no == "yes",
        "label": "Age of fifth child",
    },
    {
        "type": "input",
        "var_name": "annual_amount_of_educational_assistance",
        "conditional_on": lambda: config.providing_substantial_assistance_to_children_yes_or_no
        == "yes",
        "label": "Annual amount of educational assistance ($)",
    },
    {
        "type": "input",
        "var_name": "age_of_providing_initial_educational_assistance",
        "conditional_on": lambda: config.providing_substantial_assistance_to_children_yes_or_no
        == "yes",
        "label": "Age of child when first providing significant educational assistance",
    },
    {
        "type": "input",
        "var_name": "years_of_providing_educational_assistance",
        "conditional_on": lambda: config.providing_substantial_assistance_to_children_yes_or_no
        == "yes",
        "label": "Number of years of providing educational assistance",
    },
    {
        "type": "input",
        "var_name": "amount_of_one_off_assistance_to_children",
        "conditional_on": lambda: config.providing_substantial_assistance_to_children_yes_or_no
        == "yes",
        "label": "Amount of one-off assistance to children ($)",
    },
    {
        "type": "input",
        "var_name": "age_of_one_off_assistance_to_children",
        "conditional_on": lambda: config.providing_substantial_assistance_to_children_yes_or_no
        == "yes",
        "label": "Age of child when providing one-off assistance to children",
    },
]