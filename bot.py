import asyncio
import os
import threading
from aiogram import Bot, Dispatcher
from app import app  # Flask app import
from logging import basicConfig, INFO

# --- CONFIGURATION (Environment Variables) ---
# Render ke Dashboard mein ye Settings > Environment Variables mein daalein
API_TOKEN = os.getenv("API_TOKEN", "Aapka_Default_Token_Yahan")
ADMIN_IDS = [int(x) for x in os.getenv("ADMIN_IDS", "6265981509").split(",")]

# Logging
basicConfig(level=INFO)

# --- BOT SETUP ---
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# [Yahan aapka pura functional code (States, DB, Handlers) aayega]
# Jo code aapne upar diya hai, wahi use karein, bas token aur admin ids variables se uthayein.

async def main():
    print("Bot is starting...")
    await dp.start_polling(bot)

# Flask ko alag thread mein chalana taaki Render port open rakhe
def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

if __name__ == "__main__":
    # Start Flask thread
    threading.Thread(target=run_flask, daemon=True).start()
    # Start Bot
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot Stopped!")
      
