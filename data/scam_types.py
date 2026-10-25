"""Static reference content for the Common Scams page: frequent scam
patterns, and organizations scammers often impersonate (the real
organizations are legitimate - it's unsolicited contact claiming to be
them that's the red flag)."""

COMMON_SCAM_TYPES = [
    ("Government impersonation", "A caller or text claims to be the IRS, Social Security, or Medicare, demanding immediate payment or threatening arrest or loss of benefits."),
    ("Tech support scams", "A pop-up or call claims your computer is infected and asks you to call a number, pay for a “fix,” or install remote-access software."),
    ("Grandparent or family emergency scams", "A caller claims to be a grandchild or relative in trouble, asking for money urgently and to keep it secret from the rest of the family."),
    ("Romance scams", "Someone met online builds a relationship over time, then asks for money for an emergency, travel, or an investment."),
    ("Prize or lottery scams", "You're told you've won money or a prize, but must pay a fee or taxes first to receive it."),
    ("Phishing emails and texts", "A message that looks like it's from your bank or a delivery company asks you to click a link and “verify” your account."),
    ("Investment and cryptocurrency scams", "Promises of guaranteed high returns with little or no risk, often with pressure to act immediately."),
    ("Fake charity requests", "Especially after a disaster or crisis, pressuring you to donate immediately, often by phone or text."),
    ("Overpayment or fake check scams", "You're sent a check for more than expected and asked to wire back the “extra” amount, before the check turns out to be fake."),
]

ORGANIZATIONS_SCAMMERS_IMPERSONATE = [
    ("The IRS or other tax agencies", "The real IRS does not call demanding immediate payment, threaten arrest, or ask for gift cards. It contacts people by mail first."),
    ("Social Security Administration", "The real SSA will not call threatening to suspend or cancel your Social Security number."),
    ("Medicare", "The real Medicare will not call asking you to “verify” your Medicare number or offer free equipment in exchange for it."),
    ("Your bank or credit card company", "A real bank will not ask for your full password or a one-time verification code over the phone."),
    ("Tech companies (Microsoft, Apple, Amazon, etc.)", "These companies do not call you unprompted about a virus or account problem."),
    ("Law enforcement", "Real police do not call demanding payment by gift card or wire transfer to avoid arrest."),
    ("Utility companies", "Real utility companies do not threaten same-day disconnection while demanding immediate gift-card payment."),
]
