# Automated Niche Brief Shop

This starter publishes a daily, AI-assisted niche brief to GitHub Pages and optionally announces it in Telegram. It is intentionally a **content workflow**, not a promise of income. Review an initial batch before selling it and comply with the terms of every data source and platform.

## What it does

1. Fetches the current top stories from the public Hacker News API (no key).
2. Uses Gemini to turn those sources into an original, practical brief for a specific paying audience.
3. Creates a web page with your hosted Razorpay payment link.
4. Commits the new page and deploys it to GitHub Pages. Optionally posts an announcement through a Telegram bot.

## One-time setup

1. Create a new GitHub repository and copy every file in this folder into it.
2. In GitHub, open **Settings → Actions → General → Workflow permissions**, select **Read and write permissions**, and save.
3. In **Settings → Pages**, set Source to **GitHub Actions**.
4. Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey). The free tier and model availability can change; `GEMINI_MODEL` is configurable.
5. In Telegram, create a bot with `@BotFather`; add it as an administrator to your channel. Use an ID such as `@your_channel` for a public channel or its numeric `-100...` ID for a private channel.
6. Create a Razorpay Payment Page or Payment Link for your product, complete the required KYC, and copy its hosted URL. Razorpay charges transaction fees, so this is not zero-cost per sale.
7. Add these GitHub repository secrets under **Settings → Secrets and variables → Actions**:

   - `GEMINI_API_KEY` (required)
   - `RAZORPAY_PAYMENT_LINK` (required for the buy button)
   - `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` (optional)

   Optional repository variables: `NICHE`, `AUDIENCE`, `OFFER_NAME`, `PRICE_TEXT`, and `GEMINI_MODEL`.
8. On the **Actions** tab, run `Publish daily brief` once using **Run workflow**. Check the generated page before marketing it.

## Local test (PowerShell)

```powershell
$env:GEMINI_API_KEY = "..."
$env:RAZORPAY_PAYMENT_LINK = "https://rzp.io/l/..."
python scripts/fetch_trends.py
python scripts/generate_product.py
python scripts/build_site.py
```

Then open `site/index.html`. To send Telegram in a local test, also set the two Telegram variables and run `python scripts/publish.py`.

## Operating safely

The script cites every source link, asks the model not to invent facts, and saves raw inputs for audit. Still, AI output can be wrong: sell it as research assistance, not professional investment, medical, legal, or financial advice. Do not repost paywalled text or scrape sites that disallow automation.

## Customisation

Edit `config.json` to change the niche, audience, offer, price label, number of sources, or schedule. GitHub Actions cron is UTC; the included `30 3 * * 1-5` is 09:00 IST on weekdays (IST has no daylight saving time).
