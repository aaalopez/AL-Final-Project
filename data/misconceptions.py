"""Common financial misconceptions for the Misconceptions section."""

MISCONCEPTIONS = [
    ("ss_bankrupt", "Social Security is going bankrupt and I'll get nothing."),
    ("reverse_mortgage_bank_owns_home", "A reverse mortgage means the bank immediately owns your home."),
    ("all_debt_bad", "All debt is bad and should be avoided entirely."),
    ("need_lot_to_invest", "You need a lot of money to start investing."),
    ("savings_as_good_as_cd", "Keeping money in a regular savings account is just as good as a CD or high-yield account."),
    ("will_avoids_probate", "Having a will means your estate automatically avoids probate."),
    ("medicare_covers_long_term_care", "Medicare covers long-term nursing home care."),
]


def get_misconception_label(slug):
    for s, text in MISCONCEPTIONS:
        if s == slug:
            return text
    return None
