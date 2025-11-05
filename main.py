# main.py — ATLAS WAR (basic interactive bot with inline menu)
import os
import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token from environment (Render)
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    logger.error("TOKEN not set in environment. Please add TOKEN in Render Environment variables.")

DATA_FILE = "players.json"

# Data helpers
def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error("Error reading data file: %s", e)
        return {}

def save_data(data):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logger.error("Error writing data file: %s", e)

# Main menu layout
def main_menu():
    keyboard = [
        [InlineKeyboardButton("🪙 منابع", callback_data="resources")],
        [InlineKeyboardButton("⚔️ حمله", callback_data="attack"),
         InlineKeyboardButton("🛡️ ارتقا", callback_data="upgrade")],
        [InlineKeyboardButton("🏰 اتحاد", callback_data="alliance")]
    ]
    return InlineKeyboardMarkup(keyboard)

# /start command
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    data = load_data()
    uid = str(user.id)
    if uid not in data:
        data[uid] = {"gold": 100, "army": 10, "level": 1}
        save_data(data)

    update.message.reply_text(
        f"🎮 خوش اومدی به ATLAS WAR، {user.first_name}!\nاز منو زیر یکی رو انتخاب کن:",
        reply_markup=main_menu()
    )

# Callback button handler
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = query.from_user
    uid = str(user.id)
    data = load_data()
    player = data.get(uid, {"gold": 0, "army": 0, "level": 0})

    action = query.data
    if action == "resources":
        msg = f"💰 طلا: {player['gold']}\n⚔️ ارتش: {player['army']}\n🏅 سطح: {player['level']}"
    elif action == "attack":
        if player["army"] <= 0:
            msg = "⚠️ تو ارتشی نداری که حمله کنی!"
        else:
            player["gold"] += 20
            player["army"] -= 1
            msg = "⚔️ حمله انجام شد — ۲۰ طلا گرفتید، ۱ سرباز از دست رفت."
    elif action == "upgrade":
        cost = 100
        if player["gold"] >= cost:
            player["level"] += 1
            player["gold"] -= cost
            msg = f"🏅 تبریک! سطحت شد {player['level']}."
        else:
            msg = f"💸 طلا کافی نیست — نیاز به {cost} طلا داری."
    elif action == "alliance":
        msg = "🤝 سیستم اتحاد هنوز فعال نشده — به‌زودی!"
    else:
        msg = "❓ گزینهٔ نامشخص."

    data[uid] = player
    save_data(data)

    try:
        query.answer()
        query.edit_message_text(msg, reply_markup=main_menu())
    except Exception as e:
        logger.error("Error editing message: %s", e)

# /me command
def me(update: Update, context: CallbackContext):
    user = update.effective_user
    data = load_data()
    p = data.get(str(user.id), {"gold": 0, "army": 0, "level": 0})
    update.message.reply_text(f"💠 اطلاعات شما:\n💰 طلا: {p['gold']}\n⚔️ ارتش: {p['army']}\n🏅 سطح: {p['level']}")

# Runner
def main():
    if not TOKEN:
        logger.error("TOKEN not set — exiting.")
        return

    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("me", me))
    dp.add_handler(CallbackQueryHandler(button))

    logger.info("✅ ATLAS WAR Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
