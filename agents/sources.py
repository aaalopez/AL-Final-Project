"""Shared whitelist of official top-level source URLs.

Used by any agent that cites a source, so it can never fabricate a
specific deep-page URL (which cannot be verified and may not exist) -
only point to a stable, guaranteed-valid homepage instead.
"""

TRUSTED_SOURCES = [
    ("https://www.irs.gov", "taxes"),
    ("https://www.ssa.gov", "Social Security"),
    ("https://www.medicare.gov", "Medicare"),
    ("https://www.consumerfinance.gov", "scams, consumer financial protection, general topics"),
    ("https://www.fdic.gov", "bank deposits/insurance"),
    ("https://www.sec.gov", "investments/securities"),
    ("https://www.finra.org", "brokers/investment products"),
]


def citation_instructions(max_links=1):
    """Return system-prompt text instructing an agent to cite only the
    trusted top-level homepages above, never a deeper/specific URL."""
    lines = "\n".join(f"   - {url} ({topic})" for url, topic in TRUSTED_SOURCES)
    plural = "s" if max_links != 1 else ""
    return (
        f"Include up to {max_links} source link{plural} where relevant, but "
        "ONLY as one of these exact top-level homepage URLs — never a "
        "specific article, search result, or deeper page path, since a "
        "more specific URL cannot be verified and may not exist:\n"
        f"{lines}\n"
        "Pick whichever fit the topic, format as a Markdown link with a "
        "plain label (e.g. 'the official Medicare website'), and say what "
        "to search for or look at once there. Never output any URL that "
        "isn't exactly one of the homepages above, and never claim you "
        "checked a page live."
    )
