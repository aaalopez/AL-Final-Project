"""Shared Portkey-routed OpenAI client for all agents.

Per the course assignment spec: use PORTKEY_API_KEY with the gpt-6-luna
model only. Looks for .env in this repo folder first, then one level up.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import APIError, OpenAI
from portkey_ai import PORTKEY_GATEWAY_URL, createHeaders

from agents import usage_log


class AgentError(Exception):
    """Raised when the model call fails (rate limit, content filter, network, etc.)."""

REPO_ROOT = Path(__file__).resolve().parent.parent

_local_env = REPO_ROOT / ".env"
_parent_env = REPO_ROOT.parent / ".env"
if _local_env.exists():
    load_dotenv(_local_env)
elif _parent_env.exists():
    load_dotenv(_parent_env)

PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
if not PORTKEY_API_KEY:
    raise RuntimeError(
        "PORTKEY_API_KEY not found. Add it to a .env file in this folder "
        "or the folder one level above."
    )

MODEL = "gpt-6-luna"

client = OpenAI(
    api_key="unused",
    base_url=PORTKEY_GATEWAY_URL,
    default_headers=createHeaders(api_key=PORTKEY_API_KEY),
)


def chat(messages, label="unknown"):
    """Call the course model and return (text, usage_dict).

    gpt-6-luna only supports the default temperature (1), so no
    temperature parameter is sent.

    Raises AgentError (instead of letting the raw API error crash the
    Dash callback) if the call fails, e.g. the provider's content filter
    rejects the input, or a transient API/network error occurs.

    `label` identifies the calling agent/section (e.g.
    "tutor.explain_topic") and is recorded, along with token usage and
    estimated cost, to logs/usage_log.csv for the report's Tokenomics
    section. This logging is not shown anywhere in the app UI.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
    except APIError as exc:
        raise AgentError(str(exc)) from exc
    usage = response.usage
    usage_dict = {
        "prompt_tokens": getattr(usage, "prompt_tokens", None),
        "completion_tokens": getattr(usage, "completion_tokens", None),
        "total_tokens": getattr(usage, "total_tokens", None),
        "cached_tokens": getattr(
            getattr(usage, "prompt_tokens_details", None), "cached_tokens", None
        ),
    }
    usage_log.log_call(label, MODEL, usage_dict)
    return response.choices[0].message.content, usage_dict
