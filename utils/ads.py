# utils/ads.py
from telegram import Update

async def show_ad(update: Update):
    ad_msg = "📢 Sponsored: Check out BijanoPro for unlimited tools! https://t.me/bijanobot"
    await update.message.reply_text(ad_msg)
