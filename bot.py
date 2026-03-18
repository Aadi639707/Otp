import asyncio
import json
import os
import logging
import threading
from datetime import datetime
from typing import Optional
from flask import Flask

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# ─── FLASK SERVER FOR RENDER 24/7 ───
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is Running Live!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# ─── CONFIGURATION ───
# Render ke Environment Variables mein API_TOKEN set karein
API_TOKEN = os.environ.get("API_TOKEN", "8095207818:AAHlapXeaJwCMHosdn12zD9uMgLV7iRNLxI")
ADMIN_IDS = [6265981509, 8306853454]
CHANNEL_ID = "@yonko_crew"
CHANNEL_LINK = "https://t.me/yonko_crew"
SUPPORT_USER = "@senpai_gc"
DB_FILE = "database.json"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
log = logging.getLogger(__name__)

# ─── DATABASE LOGIC ───
DEFAULT_DB = {
    "users": {},
    "categories": [
        {"id": 1, "name": "USA Session",   "flag": "🇺🇸", "price": 150, "type": "session"},
        {"id": 2, "name": "India Session", "flag": "🇮🇳", "price": 200, "type": "session"},
        {"id": 3, "name": "USA Account",   "flag": "🇺🇸", "price": 100, "type": "account"},
        {"id": 4, "name": "India Account", "flag": "🇮🇳", "price": 120, "type": "account"},
        {"id": 5, "name": "WhatsApp SMS",  "flag": "📱",  "price": 50,  "type": "whatsapp"},
    ],
    "stock": [],
    "settings": {
        "usdt_rate": 89.0,
        "upi_id": "your-upi@id",
        "min_deposit": 50
    },
    "pending_deposits": {},
    "promos": {}
}

def load_db() -> dict:
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f: json.dump(DEFAULT_DB, f)
        return DEFAULT_DB
    with open(DB_FILE, "r") as f: return json.load(f)

def save_db(data: dict):
    with open(DB_FILE, "w") as f: json.dump(data, f, indent=2)

def get_or_create_user(user_id: int, username: str = "Unknown"):
    db = load_db()
    uid = str(user_id)
    if uid not in db["users"]:
        db["users"][uid] = {"username": username, "balance": 0.0, "spent": 0.0, "purchases": [], "joined": datetime.now().isoformat()}
        save_db(db)
    return db["users"][uid]

# ─── STATES & BOT SETUP ───
class DepositState(StatesGroup):
    waiting_for_ss = State()

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# ─── HANDLERS ───
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user = get_or_create_user(message.from_user.id, message.from_user.username)
    kb = [
        [KeyboardButton(text="📦 Sessions"), KeyboardButton(text="💰 Deposit")],
        [KeyboardButton(text="🧾 My Profile"), KeyboardButton(text="👨‍💼 Support")]
    ]
    main_kb = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer(f"Welcome {message.from_user.first_name} to Yonko Crew Store!", reply_markup=main_kb)

@dp.message(F.text == "💰 Deposit")
async def deposit_cmd(message: types.Message, state: FSMContext):
    db = load_db()
    await message.answer(f"Send Payment to: {db['settings']['upi_id']}\nThen send screenshot here.")
    await state.set_state(DepositState.waiting_for_ss)

# [Note: Aapka baki saara logic yahan continue hoga...]

async def main():
    log.info("Bot starting...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    # Start Flask Thread
    threading.Thread(target=run_web, daemon=True).start()
    # Run Bot
    asyncio.run(main())
