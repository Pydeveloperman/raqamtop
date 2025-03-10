import asyncio
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "7416227505:AAHGGaAsnfFybR66qkD5e8thztAYNs5Mc-Q"  # Bu yerga o'z Telegram bot tokeningizni qo'ying

bot = Bot(token=TOKEN)
dp = Dispatcher()

# O'yin uchun ma'lumotlar
games = {}  # {user_id: {"target": son, "attempts": urinishlar_soni}}

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("🎮 Salom! Men son topish o'yin botiman.\n"
                         "O'yinni boshlash uchun /game buyrug'ini kiriting!")

@dp.message(Command("game"))
async def start_game(message: Message):
    user_id = message.from_user.id

    # Agar foydalanuvchi oldin o‘yin boshlagan bo‘lsa, uni tozalaymiz
    games[user_id] = {"target": random.randint(1, 100), "attempts": 0}
    
    await message.answer("🎲 Men 1 dan 100 gacha bo'lgan bir sonni o'yladim. Uni topishga harakat qiling!\n"
                         "💡 Javobingizni yozing.")

@dp.message()
async def check_guess(message: Message):
    user_id = message.from_user.id

    # Foydalanuvchi o'yinda bo'lmasa, unga xabar beramiz
    if user_id not in games:
        await message.answer("⛔ Siz hali o'yinni boshlamagansiz! Iltimos, /game buyrug'ini kiriting.")
        return

    try:
        guess = int(message.text)
    except ValueError:
        await message.answer("❌ Iltimos, faqat raqam kiriting!")
        return

    games[user_id]["attempts"] += 1
    target = games[user_id]["target"]

    if guess < target:
        await message.answer("🔼 Kattaroq son kiriting!")
    elif guess > target:
        await message.answer("🔽 Kichikroq son kiriting!")
    else:
        attempts = games[user_id]["attempts"]
        await message.answer(f"🎉 Tabriklaymiz! Siz {attempts} urinishda to'g'ri sonni topdingiz! 🎯")
        del games[user_id]  # O'yin tugadi, ma'lumotni o‘chirib tashlaymiz.

# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
