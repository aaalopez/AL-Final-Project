"""Investing in My Kids: ways to save or invest on behalf of a child,
such as for education or a head start as an adult."""

KIDS_INVESTING_TOPICS = [
    ("529_plan", "529 College Savings Plans"),
    ("custodial_account", "Custodial Accounts (UGMA/UTMA)"),
    ("coverdell_esa", "Coverdell Education Savings Accounts (ESA)"),
    ("roth_ira_for_teen", "Roth IRA for a Working Teen"),
    ("savings_bonds_education", "U.S. Savings Bonds for Education"),
    ("prepaid_tuition", "Prepaid Tuition Plans"),
    ("trusts_for_children", "Trusts for Children"),
    ("kids_savings_habit", "Starting a Kids' Savings Habit"),
]


def get_kids_investing_label(slug):
    for s, text in KIDS_INVESTING_TOPICS:
        if s == slug:
            return text
    return None
