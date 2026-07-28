"""Fetch public Hacker News items. No scraping or API key is required."""
import json
from urllib.request import Request, urlopen

from common import DATA, config, today

API = "https://hacker-news.firebaseio.com/v0"


def get_json(url):
    request = Request(url, headers={"User-Agent": "NicheBriefBot/1.0 (educational research)"})
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def main():
    DATA.mkdir(exist_ok=True)
    limit = int(config().get("source_limit", 8))
    ids = get_json(f"{API}/topstories.json")[:limit * 3]
    stories = []
    for item_id in ids:
        item = get_json(f"{API}/item/{item_id}.json")
        if item and item.get("type") == "story" and item.get("title"):
            stories.append({
                "title": item["title"],
                "url": item.get("url") or f"https://news.ycombinator.com/item?id={item_id}",
                "hn_url": f"https://news.ycombinator.com/item?id={item_id}",
                "score": item.get("score", 0),
                "comments": item.get("descendants", 0),
            })
        if len(stories) == limit:
            break
    if not stories:
        raise RuntimeError("No public trend items were returned.")
    out = DATA / f"trends-{today()}.json"
    out.write_text(json.dumps(stories, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Saved {len(stories)} sources to {out}")


if __name__ == "__main__":
    main()
