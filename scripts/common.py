import html
import json
import os
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
SITE = ROOT / "site"


def config():
    values = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    # GitHub variables can override non-secret, commercial wording without a code change.
    for key in ("NICHE", "AUDIENCE", "OFFER_NAME", "PRICE_TEXT", "GEMINI_MODEL"):
        if os.getenv(key):
            values[key.lower()] = os.environ[key]
    return values


def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def esc(value):
    return html.escape(str(value), quote=True)
