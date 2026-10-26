"""Token pricing for cost estimates.

REAL RATE, derived from the Portkey dashboard's actual billed cost for
two real calls (2026-10-26), not a guess:
  - 352 tokens -> $0.0001  (exact match: the A/B-test "capped" Tutor
    Agent call in logs/usage_log.csv, 244 prompt + 108 completion)
  - ~1,300 tokens -> $0.0005 (closely matches the 1,355-token chat.ask
    call in logs/usage_log.csv, 583 prompt + 772 completion)
Token-weighted blended rate across both: ($0.0001 + $0.0005) /
((352 + 1355) / 1000) = $0.000352 per 1K tokens. gpt-6-luna's billing
isn't broken out by input/output/cached on the dashboard, so this one
blended rate is used for all three constants below rather than three
separately-sourced numbers - the best real anchor available, in place
of the GPT-4o-mini-level placeholder this module used before.
"""

PRICE_PER_1K_INPUT_TOKENS = 0.000352
PRICE_PER_1K_CACHED_INPUT_TOKENS = 0.000352
PRICE_PER_1K_OUTPUT_TOKENS = 0.000352


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
