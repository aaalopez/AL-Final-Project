"""Local, app-invisible log of every model call's token usage and estimated cost.

Not wired into the UI on purpose - this is raw data for the report's
Tokenomics section (real measured tokens/cost per run), not something
end users need to see. Writes one CSV row per call to logs/usage_log.csv.
"""

import csv
from datetime import datetime, timezone
from pathlib import Path

from data.pricing import estimate_cost

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_FILE = LOG_DIR / "usage_log.csv"

FIELDNAMES = [
    "timestamp_utc",
    "label",
    "model",
    "prompt_tokens",
    "cached_tokens",
    "completion_tokens",
    "total_tokens",
    "estimated_cost_usd",
]


def log_call(label, model, usage):
    """Append one row for a completed model call. Silently no-ops on failure
    so logging issues never break the app."""
    try:
        LOG_DIR.mkdir(exist_ok=True)
        is_new = not LOG_FILE.exists()
        with open(LOG_FILE, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            if is_new:
                writer.writeheader()
            cost = estimate_cost(usage)
            writer.writerow(
                {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "label": label,
                    "model": model,
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "cached_tokens": usage.get("cached_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                    "estimated_cost_usd": f"{cost:.6f}" if cost is not None else "",
                }
            )
    except OSError:
        pass
