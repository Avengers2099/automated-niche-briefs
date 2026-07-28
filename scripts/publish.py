"""Optional Telegram channel announcement via the official Bot API."""
import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from common import config, today


def main():
    token, chat_id = os.getenv("TELEGRAM_BOT_TOKEN"), os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        print("Telegram secrets not set; skipping Telegram publish.")
        return
    repo = os.getenv("GITHUB_REPOSITORY", "YOUR_GITHUB_USERNAME/YOUR_REPOSITORY")
    url = f"https://{repo.split('/')[0]}.github.io/{repo.split('/')[1]}/"
    settings = config()
    message = f"New {settings['offer_name']} is live: {url}\n{settings['price_text']} · Secure payment link on the page."
    body = urlencode({"chat_id": chat_id, "text": message, "disable_web_page_preview": "false"}).encode()
    request = Request(f"https://api.telegram.org/bot{token}/sendMessage", data=body, method="POST")
    with urlopen(request, timeout=30) as response:
        result = json.load(response)
    if not result.get("ok"):
        raise RuntimeError(f"Telegram rejected message: {result}")
    print(f"Telegram announcement sent for {today()}")


if __name__ == "__main__":
    main()
