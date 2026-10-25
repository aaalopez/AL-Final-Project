"""Family-Bridge Agent: turns another agent's output into a shareable
plain-language summary for the 'For My Kids' section."""

from agents.client import chat

FAMILY_BRIDGE_SYSTEM_PROMPT = (
    "You help an older adult communicate a financial topic or a possible "
    "scam encounter to their adult children or family, in a short message "
    "they could text or email as-is. Tone: calm, factual, not alarmist, "
    "first person from the older adult's perspective. No jargon. "
    "Keep it under 120 words. Do not include passwords, PINs, account or "
    "full card numbers, Social Security numbers, or verification codes, "
    "even if they appear in the source. Do not add unsupported claims, "
    "guarantees, or pressure to take action. Preserve the user's choice "
    "about whether to share the message."
)


def summarize_for_family(context_label, agent_output, recipient=None):
    """Return (text, usage_dict) with a shareable family-facing summary.

    `recipient` is a free-text description of who the message is for
    (e.g. "my daughter Sarah", "my son", "a close friend"), used only to
    address the message naturally - never to add any identifying detail
    beyond what the user themselves typed.
    """
    recipient = (recipient or "").strip() or "a family member"
    user_prompt = (
        f"Context: {context_label}\n\n"
        f"Who this is for: {recipient}\n\n"
        f"Original analysis/explanation to summarize:\n{agent_output}\n\n"
        "Write the shareable message now, addressed naturally to this "
        "person (e.g. a greeting that fits who they are, if appropriate) "
        "without inventing any detail about them beyond what was given."
    )
    return chat(
        [
            {"role": "system", "content": FAMILY_BRIDGE_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        label="family_bridge.summarize_for_family",
    )
