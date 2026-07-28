"""Render a small static sales page; GitHub Pages serves the site for free."""
import os
import re
from pathlib import Path

from common import SITE, config, esc, today


def markdown_to_html(markdown):
    # Deliberately small renderer: generated content is escaped before limited formatting.
    lines, result, in_list = markdown.splitlines(), [], False
    for line in lines:
        safe = esc(line)
        safe = re.sub(r"\[([^]]+)\]\((https?://[^ )]+)\)", r'<a href="\2" rel="noopener noreferrer" target="_blank">\1</a>', safe)
        if safe.startswith("# "):
            result.append(f"<h1>{safe[2:]}</h1>")
        elif safe.startswith("## "):
            result.append(f"<h2>{safe[3:]}</h2>")
        elif safe.startswith("- "):
            if not in_list: result.append("<ul>"); in_list = True
            result.append(f"<li>{safe[2:]}</li>")
        else:
            if in_list: result.append("</ul>"); in_list = False
            if safe.strip(): result.append(f"<p>{safe}</p>")
    if in_list: result.append("</ul>")
    return "\n".join(result)


def main():
    settings, date = config(), today()
    brief = (Path("data") / f"brief-{date}.md").read_text(encoding="utf-8")
    payment = os.getenv("RAZORPAY_PAYMENT_LINK", "#")
    SITE.mkdir(exist_ok=True)
    page = f'''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(settings['offer_name'])}</title><link rel="stylesheet" href="style.css"><body><main>
<p class="eyebrow">{esc(date)} · {esc(settings['audience'])}</p>{markdown_to_html(brief)}
<aside><h2>Buy the premium edition</h2><p>{esc(settings['offer_name'])} — {esc(settings['price_text'])}</p><a class="button" href="{esc(payment)}" rel="noopener noreferrer" target="_blank">Buy securely</a><p class="fine">Configure the Razorpay link to describe the premium bundle or subscription it delivers. Payments are processed by Razorpay. This is educational research, not professional advice.</p></aside>
</main></body></html>'''
    (SITE / f"{date}.html").write_text(page, encoding="utf-8")
    (SITE / "index.html").write_text(page, encoding="utf-8")
    print(f"Rendered site/{date}.html and site/index.html")


if __name__ == "__main__":
    main()
