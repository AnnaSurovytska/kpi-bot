from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import datetime

TOKEN = os.getenv("TOKEN")

KPI_LINK = 'https://docs.google.com/spreadsheets/d/187czH5iolCe_wmARbZ_blpQjzJQHQ7__/edit?gid=1652687997'

KPI_INFO = {
    "Что такое KPI": "📊 KPI — это ключевые показатели эффективности...",
    "Как писать": "✍️ Пиши задачи по SMART...",
    "Критерии": "✅ Задача считается выполненной, если выполнена на 100%, в срок и качественно."
}

keyboard = [
    ["Что такое KPI", "Как писать"],
    ["Критерии", "Напомнить"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу тебе не забыть про KPI и подскажу, как правильно их оформить.",
        reply_markup=markup
    )

# Обработка нажатий по кнопкам
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in KPI_INFO:
        await update.message.reply_text(KPI_INFO[text])
    elif text == "Напомнить":
        await update.message.reply_text(f"⏰ Не забудь внести KPI в таблицу!\n👉 {KPI_LINK}")
    else:
        await update.message.reply_text("Не понимаю команду. Попробуй нажать кнопку 👇")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("remind", button_handler))  # для тесту, поки що
app.add_handler(CommandHandler("what_is_kpi", button_handler))  # опціонально
app.add_handler(CommandHandler("how_to_write", button_handler))  # опціонально
app.add_handler(CommandHandler("criteria", button_handler))  # опціонально

# Головний обробник тексту (від кнопок)
app.add_handler(CommandHandler(None, button_handler))  # на випадок, якщо команда, але без /start
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))

app.run_polling()
