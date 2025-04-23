from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os
import datetime

# Получаем токен из переменных окружения
TOKEN = os.getenv("TOKEN")

# Ссылка на таблицу KPI
KPI_LINK = 'https://docs.google.com/spreadsheets/d/187czH5iolCe_wmARbZ_blpQjzJQHQ7__/edit?gid=1652687997'

# KPI информация
KPI_INFO = {
    "what_is_kpi": "📊 KPI — это ключевые показатели эффективности. Они показывают, насколько успешно человек достигает целей.",
    "how_to_write": "✍️ Пиши задачи по SMART: конкретно, измеримо, достижимо, релевантно, ограничено по времени.",
    "criteria": "✅ Задача выполнена, если сделана на 100%, в срок и с нужным качеством."
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я помогу тебе не забыть про KPI и подскажу, как правильно их оформить.")

# Команды-информация
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cmd = update.message.text.replace("/", "")
    if cmd in KPI_INFO:
        await update.message.reply_text(KPI_INFO[cmd])
    else:
        await update.message.reply_text("Не знаю такую команду. Попробуй /what_is_kpi, /how_to_write или /criteria.")

# Напоминание
async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"⏰ Не забудь внести KPI в таблицу!\nВот ссылка: {KPI_LINK}")

# Инициализация бота
app = ApplicationBuilder().token(TOKEN).build()

# Обработчики команд
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("what_is_kpi", info))
app.add_handler(CommandHandler("how_to_write", info))
app.add_handler(CommandHandler("criteria", info))
app.add_handler(CommandHandler("remind", remind))

# Запуск бота
app.run_polling()
