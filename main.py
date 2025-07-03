import asyncio
import logging
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiohttp import web

# 🔐 Твой токен
API_TOKEN = "7828982013:AAHRV1sV5OwWnx0aceawR4Ppfimjx3lrxgo"

bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

LANGUAGES = {
    "🇷🇺 Русский": "ru",
    "🇬🇧 English": "en",
    "🇷🇴 Română": "ro"
}

# Главное меню
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🌐 Выбрать страну")],
            [KeyboardButton("📖 Инструкция"), KeyboardButton("📢 Отзывы")],
            [KeyboardButton("👤 Мой профиль")]
        ],
        resize_keyboard=True
    )

# Меню выбора страны
def country_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🌍 Материки"), KeyboardButton("🏳 Страны")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

# Меню континентов
def continent_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🌍 Африка"), KeyboardButton("🌏 Азия")],
            [KeyboardButton("🌄 Балканы"), KeyboardButton("🏝 Карибские острова")],
            [KeyboardButton("🇪🇺 Европа"), KeyboardButton("🇪🇺+🌄 Европа + Балканы")],
            [KeyboardButton("🌐 Global"), KeyboardButton("🌎 Латинская Америка")],
            [KeyboardButton("🕌 Средний Восток"), KeyboardButton("🇺🇸 Северная Америка")],
            [KeyboardButton("🌊 Океания")],
            [KeyboardButton("⬅️ Назад")]
        ],
        resize_keyboard=True
    )

@dp.message(Command("start"))
@dp.message(Command("restart"))
async def start(message: Message):
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(lang)] for lang in LANGUAGES],
        resize_keyboard=True
    )
    await message.answer("👋 Добро пожаловать в UniSIM!\n\nПожалуйста, выберите язык:", reply_markup=kb)

@dp.message(F.text.in_(LANGUAGES))
async def language_selected(message: Message):
    await message.answer_photo(
        photo="https://via.placeholder.com/600x300.png?text=Welcome+to+UniSIM",  # сюда можно вставить твоё фото
        caption=(
            "🌐 <b>UniSIM</b> — ваш цифровой ключ к интернету по всему миру!\n\n"
            "📱 Получите eSIM без похода в салон\n"
            "🌍 Более 120+ стран по низким ценам\n"
            "🧳 Идеально для путешествий, удалённой работы и бизнеса\n\n"
            "❓ Список стран по регионам — в разделе «Помощь».\n\n"
            "👇 Выберите нужный раздел:"
        ),
        reply_markup=main_menu()
    )

@dp.message(F.text == "🌐 Выбрать страну")
async def choose_country(message: Message):
    await message.answer("Выберите способ:", reply_markup=country_menu())

@dp.message(F.text == "🌍 Материки")
async def show_continents(message: Message):
    await message.answer("Выберите регион:", reply_markup=continent_menu())

@dp.message(F.text == "🏳 Страны")
async def choose_by_country(message: Message):
    await message.answer("🔎 Введите название страны для поиска:")

@dp.message(F.text == "⬅️ Назад")
async def back_to_main(message: Message):
    await message.answer("Вы вернулись в главное меню:", reply_markup=main_menu())

@dp.message(F.text == "📖 Инструкция")
async def instruction(message: Message):
    await message.answer(
        "📖 <b>Как подключить eSIM:</b>\n\n"
        "1️⃣ После покупки вы получите QR-код\n"
        "2️⃣ Откройте: Настройки > Сотовая связь > Добавить eSIM\n"
        "3️⃣ Отсканируйте QR-код\n"
        "4️⃣ Подтвердите установку\n\n"
        "💡 Важно: подключитесь к Wi-Fi перед активацией!"
    )

@dp.message(F.text == "📢 Отзывы")
async def reviews(message: Message):
    await message.answer("📢 Отзывы клиентов скоро появятся здесь!\n\nТы можешь оставить свой отзыв в поддержку.")

@dp.message(F.text == "👤 Мой профиль")
async def profile(message: Message):
    await message.answer(
        f"👤 Ваш профиль:\n\n"
        f"💰 Баланс: 0.00 €\n"
        f"🕒 Время в боте: 0 дней\n"
        f"👥 Рефералы: 0\n"
        f"🛒 История покупок: пока нет"
    )

# Web-сервер для Replit
async def handle(request):
    return web.Response(text="✅ UniSIM работает")

async def main():
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

def run():
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app = web.Application()
    app.router.add_get("/", handle)
    web.run_app(app, port=8080)

if __name__ == "__main__":
    run()
  
