"""Topic taxonomy for the 101s section.

Each category maps to a list of (slug, label) sub-topics. The Tutor Agent
generates a "What it is" / "Why it matters" explanation for each sub-topic
on demand (and the app caches the result so repeat visits don't re-spend
tokens).
"""

TOPICS = {
    "retirement": {
        "label": "Retirement",
        "subtopics": [
            ("401k_basics", "401(k) basics"),
            ("401k_rollover", "Rolling over a 401(k)"),
            ("roth_ira", "Roth IRA"),
            ("traditional_ira", "Traditional IRA"),
            ("rmds", "Required Minimum Distributions (RMDs)"),
            ("withdrawal_timing", "When to start withdrawing"),
        ],
    },
    "loans": {
        "label": "Loans",
        "subtopics": [
            ("mortgages", "Mortgages"),
            ("reverse_mortgages", "Reverse mortgages"),
            ("personal_loans", "Personal loans"),
            ("medical_debt", "Medical debt"),
            ("credit_card_debt", "Credit card debt"),
        ],
    },
    "savings": {
        "label": "Savings",
        "subtopics": [
            ("emergency_fund", "Emergency funds"),
            ("high_yield_savings", "High-yield savings accounts"),
            ("cds", "Certificates of Deposit (CDs)"),
            ("budgeting_basics", "Budgeting basics"),
        ],
    },
    "social_security_medicare": {
        "label": "Social Security & Medicare",
        "subtopics": [
            ("ss_claiming", "When to claim Social Security"),
            ("ss_calculation", "How benefits are calculated"),
            ("medicare_ab", "Medicare Part A & B"),
            ("medicare_cd", "Medicare Part C & D"),
            ("medigap", "Medigap (supplemental insurance)"),
        ],
    },
    "estate_planning": {
        "label": "Estate Planning",
        "subtopics": [
            ("wills", "Wills"),
            ("power_of_attorney", "Power of attorney"),
            ("beneficiary_designations", "Beneficiary designations"),
            ("trusts", "Trusts (overview)"),
        ],
    },
    "insurance": {
        "label": "Insurance",
        "subtopics": [
            ("life_insurance", "Life insurance"),
            ("long_term_care", "Long-term care insurance"),
            ("annuities", "Annuities"),
        ],
    },
    "investments": {
        "label": "Investments",
        "subtopics": [
            ("stocks", "Stocks"),
            ("bonds", "Bonds"),
            ("etfs", "Exchange-Traded Funds (ETFs)"),
            ("mutual_funds", "Mutual Funds"),
            ("bank_products", "Bank Products (CDs)"),
            ("digital_assets", "Digital Assets (Cryptocurrency)"),
            ("options", "Options"),
            ("futures_commodities", "Futures & Commodities"),
            ("investment_life_insurance", "Life Insurance"),
            ("income_annuities", "Income Annuities"),
            ("alternative_investments", "Alternative & Emerging Investments"),
        ],
    },
}


def get_category_labels():
    """Return [(slug, label), ...] for the top-level categories, in order."""
    return [(slug, data["label"]) for slug, data in TOPICS.items()]


def get_subtopics(category_slug):
    """Return [(slug, label), ...] for a category's sub-topics."""
    return TOPICS[category_slug]["subtopics"]


def get_subtopic_label(category_slug, subtopic_slug):
    for slug, label in get_subtopics(category_slug):
        if slug == subtopic_slug:
            return label
    return None
