from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

# Отримуємо токен з середовища Render
TOKEN = os.getenv("TOKEN")

# Посилання на Google Таблицю KPI
KPI_LINK = 'https://docs.google.com/spreadsheets/d/187czH5iolCe_wmARbZ_blpQjzJQHQ7__/edit?gid=1652687997'

# Інформація для команд
KPI_INFO = {
    "Что такое KPI": "📊 KPI — это ключевые показатели эффективности. Они показывают, насколько успешно человек достигает целей.",
    "Как писать": "✍️ Пиши задачи по SMART: конкретно, измеримо, достижимо, релевантно, ограничено во времени.",
    "Критерии": "✅ Задача считается выполненной, если она сделана на 100%, в срок и с нужным качеством."
}

# Кнопки
keyboard = [
    ["Что такое KPI", "Как писать"],
    ["Критерии", "Напомнить"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу тебе не забыть про KPI и подскажу, как правильно их оформить.",
        reply_markup=markup
    )

# Обработка текстовых сообщений (нажатие кнопок)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in KPI_INFO:
        await update.message.reply_text(KPI_INFO[text])
    elif text == "Напомнить":
        await update.message.reply_text(f"⏰ Не забудь внести KPI в таблицу!\n👉 {KPI_LINK}")
    else:
        await update.message.reply_text("Пожалуйста, выбери команду с кнопки ниже 👇")

# Инициализация и запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
