# main.py

import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import config

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher(bot)

# چک عضویت در کانال
async def check_subs(user_id):
    for channel in config.REQUIRED_CHANNELS:
        member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
        if member.status not in ['member', 'administrator', 'creator']:
            return False
    return True

# استارت
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if await check_subs(message.from_user.id):
        await message.answer(config.WELCOME_MESSAGE)
    else:
        channels = "\n".join([f"📌 {ch}" for ch in config.REQUIRED_CHANNELS])
        await message.answer(f"🔒 برای استفاده از ربات باید عضو کانال‌های زیر بشی:\n\n{channels}")

# پیام ادمین به همه کاربران
@dp.message_handler(commands=['broadcast'])
async def broadcast_handler(message: types.Message):
    if message.from_user.id in config.ADMINS:
        msg = message.text.replace('/broadcast', '').strip()
        if not msg:
            await message.reply("لطفاً بعد از دستور /broadcast یک پیام بنویس")
            return
        await message.reply("✅ پیام برای همه کاربران فرستاده می‌شود (در نسخه کامل ذخیره کاربر نیاز است)")
    else:
        await message.reply("شما ادمین نیستید ❌")

# پیام خودکار
@dp.message_handler(lambda m: m.text and 'سلام' in m.text)
async def auto_reply(message: types.Message):
    await message.reply("سلام خوش اومدی 🌺")

# دریافت پیام از کاربر
@dp.message_handler()
async def echo_all(message: types.Message):
    await message.answer("پیامت دریافت شد 💬")
