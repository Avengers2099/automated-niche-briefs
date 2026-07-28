# Launch checklist

## Before connecting money

- [ ] Choose one narrow buyer: for example, "Indian dental clinics that need appointment follow-ups", not "small businesses".
- [ ] Replace the settings in `config.json` with that buyer and their desired outcome.
- [ ] Run the workflow once and personally check the brief's factual claims and source links.
- [ ] Write a plain refund and contact policy on the payment page.

## GitHub Pages

- [ ] Make a repository and upload this folder's contents (including `.github`).
- [ ] Set Actions workflow permissions to **Read and write**.
- [ ] Set Pages source to **GitHub Actions**.
- [ ] Add `GEMINI_API_KEY` and `RAZORPAY_PAYMENT_LINK` as Actions secrets.
- [ ] Start the workflow manually and confirm the Pages URL opens.

## Telegram

- [ ] Create a channel and publish at least five useful free posts before linking a product.
- [ ] Create a bot with BotFather, make it channel admin, then save its token and channel ID as secrets.
- [ ] Run the workflow manually and confirm exactly one announcement arrives.

## Payment

- [ ] Complete Razorpay KYC under the actual business/person that will receive settlements.
- [ ] Make a hosted Payment Page/Link for a clearly described product or subscription.
- [ ] Paste the URL only into `RAZORPAY_PAYMENT_LINK`; never put Razorpay key secrets in this static repository.
- [ ] Configure payment confirmation and customer-support contact in Razorpay.

## First revenue test

- [ ] Offer 10 founding subscriptions at a clearly stated introductory price.
- [ ] Talk to those buyers and revise the niche, offer, and price based on whether the brief saves time or earns them money.
- [ ] Do not automate paid fulfilment until the offer has real buyers; first validate what they actually want delivered.
