"""Common Questions: FAQ-style questions for middle-aged adults who feel
behind on or unfamiliar with personal finance basics - juggling debt,
retirement, kids, and aging parents at once, often for the first time."""

COMMON_QUESTIONS = [
    (
        "late_retirement_start",
        "I'm in my 40s or 50s with little to no retirement savings. Is it too late to start?",
    ),
    (
        "401k_vs_ira",
        "What's actually the difference between a 401(k) and an IRA?",
    ),
    (
        "debt_vs_saving",
        "I have credit card debt. Should I pay it off before saving, or do both at once?",
    ),
    (
        "emergency_fund_size",
        "How much should I actually keep in an emergency fund?",
    ),
    (
        "employer_match",
        "My employer offers a 401(k) match. What does that mean, and am I missing out if I don't contribute?",
    ),
    (
        "sandwich_generation",
        "I'm paying for my kids' expenses and helping my aging parents at the same time. How do I budget for both?",
    ),
    (
        "credit_score_basics",
        "What is a credit score, and what actually affects it?",
    ),
    (
        "finding_an_advisor",
        "Should I use a financial advisor? How do I know if I can trust one?",
    ),
    (
        "raise_what_to_do",
        "I just got a raise. What should I actually do with the extra money?",
    ),
    (
        "job_loss_debts",
        "What happens to my debts and bills if I lose my job?",
    ),
]


def get_question_label(slug):
    for s, text in COMMON_QUESTIONS:
        if s == slug:
            return text
    return None
