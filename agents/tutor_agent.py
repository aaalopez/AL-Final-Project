"""Tutor Agent: explains 101 topics and corrects misconceptions in plain language."""

from agents.client import chat
from agents.sources import citation_instructions

_cache = {}

TUTOR_SYSTEM_PROMPT = (
    "You are a patient, plain-language financial tutor for older adults. "
    "Avoid jargon; when you must use a financial term, define it immediately. "
    "Keep a warm, respectful, non-condescending tone. Use short paragraphs "
    "and simple sentences. Never recommend a specific company, product, or "
    "investment. When relevant, note that the reader should consult a "
    "licensed financial advisor for personal decisions. Give general "
    "education, not legal, tax, medical, or mental-health advice; do not "
    "diagnose, provide therapy, or recommend treatment. Respond to distress "
    "with empathy and encourage appropriate professional support. Never "
    "ask for or repeat passwords, PINs, account or full card numbers, "
    "Social Security numbers, or verification codes. Do not impersonate a "
    "bank, government agency, or human professional, and do not guarantee "
    "outcomes. Direct questions about changing rules or figures to current, "
    "authoritative sources."
)


def explain_topic(category_label, subtopic_label):
    """Return (text, usage_dict) explaining a 101 sub-topic."""
    cache_key = ("topic", category_label, subtopic_label)
    if cache_key in _cache:
        return _cache[cache_key]

    user_prompt = (
        f"Topic: {subtopic_label} (category: {category_label}).\n\n"
        "Write a short explainer with two clearly labeled parts:\n"
        "1. What it is - a plain-language definition, 2-4 sentences.\n"
        "2. Why it matters - why someone should care about this, 2-4 sentences.\n"
        "Keep the total under 200 words."
    )
    result = chat(
        [
            {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        label="tutor.explain_topic",
    )
    _cache[cache_key] = result
    return result


def explain_misconception(misconception_text):
    """Return (text, usage_dict) correcting a misconception."""
    cache_key = ("misconception", misconception_text)
    if cache_key in _cache:
        return _cache[cache_key]

    user_prompt = (
        f'A reader believes this: "{misconception_text}"\n\n'
        "Gently explain what's true and what's not, in plain language. "
        "Start with a one-sentence verdict (e.g. 'Mostly false' or "
        "'Partly true'), then explain why in 3-5 short sentences. "
        "Keep the total under 180 words."
    )
    result = chat(
        [
            {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        label="tutor.explain_misconception",
    )
    _cache[cache_key] = result
    return result


def answer_faq(question_text):
    """Return (text, usage_dict) answering a Common Questions FAQ entry."""
    cache_key = ("faq", question_text)
    if cache_key in _cache:
        return _cache[cache_key]

    user_prompt = (
        f'A reader asks: "{question_text}"\n\n'
        "This reader may feel behind or embarrassed about not knowing "
        "this already - do not make them feel that way. Answer directly "
        "and practically, in plain language, with concrete next steps "
        "where relevant. Keep the answer itself under 200 words. "
        + citation_instructions(max_links=1)
    )
    result = chat(
        [
            {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        label="tutor.answer_faq",
    )
    _cache[cache_key] = result
    return result


def explain_kids_investing(topic_label):
    """Return (text, usage_dict) explaining a way to invest/save for a child."""
    cache_key = ("kids_investing", topic_label)
    if cache_key in _cache:
        return _cache[cache_key]

    user_prompt = (
        f"Topic: {topic_label}, a way parents or grandparents can save or "
        "invest on behalf of a child.\n\n"
        "Write a short explainer with two clearly labeled parts:\n"
        "1. What it is - a plain-language definition, 2-4 sentences.\n"
        "2. Why it matters - who it's useful for and the key tradeoff or "
        "limitation to know about, 2-4 sentences.\n"
        "Keep the answer itself under 200 words. " + citation_instructions(max_links=1)
    )
    result = chat(
        [
            {"role": "system", "content": TUTOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        label="tutor.explain_kids_investing",
    )
    _cache[cache_key] = result
    return result


