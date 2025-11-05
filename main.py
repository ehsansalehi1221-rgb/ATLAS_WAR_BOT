import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.getenv("TOKEN")  # توکن از تنظیمات Render گرفته می‌شود

def start(update, context):
    update.message.reply_text("🎮 ربات شروع شد! خوش اومدی به ATLAS WAR BOT.")

def newgame(update, context):
    update.message.reply_text("🔥 یه بازی جدید شروع شد! آماده‌ای برای نبرد؟")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("newgame", newgame))

    print("✅ Bot is running...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
