"""Token pricing for cost estimates.

PLACEHOLDER RATES: gpt-6-luna is a course-specific model alias routed
through Portkey, so its real per-token billing rate isn't published.
These values are stand-ins (roughly GPT-4o-mini-level pricing) so the
app can show a cost estimate. Before writing the Tokenomics section of
the report, check the Portkey dashboard's logged cost per request (or
ask course staff) and replace these three numbers with the real rate.
"""

PRICE_PER_1K_INPUT_TOKENS = 0.00015
PRICE_PER_1K_CACHED_INPUT_TOKENS = 0.000075
PRICE_PER_1K_OUTPUT_TOKENS = 0.0006


def estimate_cost(usage):
    """Return an estimated dollar cost for one call's usage dict, or None."""
    if not usage or usage.get("total_tokens") is None:
        return None
    prompt_tokens = usage.get("prompt_tokens") or 0
    cached_tokens = usage.get("cached_tokens") or 0
    completion_tokens = usage.get("completion_tokens") or 0
    uncached_input = max(prompt_tokens - cached_tokens, 0)

    cost = (
        (uncached_input / 1000) * PRICE_PER_1K_INPUT_TOKENS
        + (cached_tokens / 1000) * PRICE_PER_1K_CACHED_INPUT_TOKENS
        + (completion_tokens / 1000) * PRICE_PER_1K_OUTPUT_TOKENS
    )
    return cost
