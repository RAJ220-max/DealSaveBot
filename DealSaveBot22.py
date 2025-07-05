import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
import re
import urllib.parse
import asyncio  # for delay

TOKEN = "7762528345:AAHLxxhC_vJBrMLheiPXjw9IZwX--7Qed2M"
AFFILIATE_TAG = "amazonpric0c2-21"
CUELINKS_PUB_ID = "208307"  # ← Replace with your real Cuelinks ID

logging.basicConfig(level=logging.INFO)

# ------------------- START -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🛍️ Product Name", callback_data='product_name')],
        [InlineKeyboardButton("🔗 Product Link", callback_data='product_link')],
        [InlineKeyboardButton("🖼️ Image of Product (coming soon)", callback_data='coming_soon')]
    ]
    await update.message.reply_text(
        "👋 Welcome to DealSaveBot!\n\n"
        "🔍 This bot helps you compare product prices from:\n"
        "✅ Amazon\n✅ Flipkart\n✅ Meesho\n✅ Snapdeal\n✅ Myntra\n✅ ShopClues\n\n"
        "📢 Join our Telegram Channel for latest deals: [DealSave1](https://t.me/DealSave1)\n\n"
        "🧠 Just give a product name or link to start!",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode='Markdown'
    )

    # 🔥 Sponsored Message after delay
    await asyncio.sleep(12)
    await update.message.reply_text(
        "🔔 *Sponsored Message* 🔔\n\n"
        "👉 Click here to check out amazing tech deals!",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🔥 VISIT SPONSOR 🔗", url="https://t.me/Amazon_ProductPriceTrackerBot")]]
        ),
        parse_mode='Markdown'
    )

# ------------------- BUTTON HANDLER -------------------

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data['mode'] = query.data

    if query.data == 'product_name':
        await query.message.reply_text("📝 Please enter the product name:")
    elif query.data in ['product_link', 'coming_soon']:
        await query.message.reply_text("🛠️ This feature is coming soon!")

# ------------------- Generate Cuelinks Link -------------------

def cuelinks_affiliate_link(url: str) -> str:
    base = "https://linksredirect.com"
    return f"{base}/?pub_id={CUELINKS_PUB_ID}&url={urllib.parse.quote_plus(url)}"

# ------------------- USER MESSAGE HANDLER -------------------

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    mode = context.user_data.get('mode')

    if not mode or mode in ['product_link', 'coming_soon']:
        await update.message.reply_text("❗ This feature is not available yet. Please select 'Product Name' to continue.")
        return

    if mode == 'product_name':
        product = urllib.parse.quote_plus(text)

        amazon_link = f"https://www.amazon.in/s?k={product}&tag={AFFILIATE_TAG}"
        flipkart_link = cuelinks_affiliate_link(f"https://www.flipkart.com/search?q={product}")
        meesho_link = cuelinks_affiliate_link(f"https://www.meesho.com/search?q={product}")
        snapdeal_link = cuelinks_affiliate_link(f"https://www.snapdeal.com/search?keyword={product}")
        myntra_link = cuelinks_affiliate_link(f"https://www.myntra.com/{urllib.parse.unquote_plus(product).replace(' ', '-')}")
        shopclues_link = cuelinks_affiliate_link(f"https://www.shopclues.com/search?q={product}")

        await update.message.reply_text(
            f"🔍 Price Comparison for: {urllib.parse.unquote_plus(product)}\n\n"
            f"🛒 Amazon:\n🔗 {amazon_link}\n\n"
            f"🛍️ Flipkart:\n🔗 {flipkart_link}\n\n"
            f"👜 Meesho:\n🔗 {meesho_link}\n\n"
            f"📦 Snapdeal:\n🔗 {snapdeal_link}\n\n"
            f"👗 Myntra:\n🔗 {myntra_link}\n\n"
            f"🧺 ShopClues:\n🔗 {shopclues_link}"
        )

        await update.message.reply_text(
            "📢 For latest deals & offers, join our Telegram Channel:\n👉 https://t.me/DealSave1"
        )

# ------------------- RUN BOT -------------------

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button_handler))
app.add_handler(MessageHandler(filters.TEXT, handle_message))
app.run_polling()
