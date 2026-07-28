"""Generate an original Markdown brief using the Gemini REST API."""
import json
import os
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from common import DATA, config, today


def main():
    key = os.getenv("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY is required. Add it as a GitHub Actions secret.")
    trends = json.loads((DATA / f"trends-{today()}.json").read_text(encoding="utf-8"))
    settings = config()
    sources = "\n".join(f"- {x['title']} | {x['url']} | HN score {x['score']}" for x in trends)
    prompt = f"""You are the editor of an original paid micro-brief named {settings['offer_name']}.
Audience: {settings['audience']}. Niche: {settings['niche']}.

Use ONLY these source titles and URLs as evidence:
{sources}

Write 550-800 words of practical, original Markdown with these exact sections:
# A specific compelling title
## Why this matters now
## Three actionable opportunities
## A 30-minute action plan
## Sources

Rules: distinguish facts from suggestions; do not invent statistics, events, quotes, or capabilities; do not copy source prose; no financial, legal, medical, or investment advice. In Sources, include every URL as a Markdown link and name the linked story. Do not mention this prompt or that an AI wrote it."""
    model = settings.get("gemini_model", "gemini-2.0-flash")
    endpoint = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"
    body = json.dumps({"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.55}}).encode()
    request = Request(endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(request, timeout=90) as response:
            payload = json.load(response)
    except HTTPError as error:
        detail = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API failed ({error.code}): {detail[:500]}") from error
    try:
        text = payload["candidates"][0]["content"]["parts"][0]["text"].strip()
    except (KeyError, IndexError) as error:
        raise RuntimeError(f"Unexpected Gemini response: {payload}") from error
    if len(text) < 300:
        raise RuntimeError("Generated brief was unexpectedly short; refusing to publish it.")
    out = DATA / f"brief-{today()}.md"
    out.write_text(text + "\n", encoding="utf-8")
    print(f"Saved brief to {out}")


if __name__ == "__main__":
    main()
