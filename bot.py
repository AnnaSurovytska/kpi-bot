from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.background import BackgroundScheduler
import os

TOKEN = os.getenv("TOKEN")

# ⚠️ Вкажи тут ID чата, куди слати нагадування (група або твій приват)
CHAT_ID = os.getenv("CHAT_ID")  # Укажи це в Render як переменную окружения

KPI_LINK = 'https://docs.google.com/spreadsheets/d/187czH5iolCe_wmARbZ_blpQjzJQHQ7__/edit?gid=1652687997'

KPI_INFO = {
    "Что такое KPI": "📊 KPI — это конкретная цифра или метрика, по которой оценивают, насколько хорошо ты справляешься со своей работой. Это как цель + цифра (или конкретное задание), по которой можно понять: достигнута задача или нет.
💡 Или, как сказал Питер Друкер: «То, что измеряется — улучшается».",
    "Как писать": "✍️ Пиши задачи по SMART - это чётко сформулированные цели, которые конкретны, измеримы, достижимы, релевантны и ограничены по времени.",
    "Критерии": "✅ Задача считается выполненной, если выполнена на 100%, в срок и качественно."
}

keyboard = [
    ["Что такое KPI", "Как писать"],
    ["Критерии", "Файл"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу тебе не забыть про KPI и подскажу, как правильно их оформить.",
        reply_markup=markup
    )

# Обработка текстов
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in KPI_INFO:
        await update.message.reply_text(KPI_INFO[text])
    elif text == "Напомнить":
        await update.message.reply_text(f"⏰ Не забудь внести KPI в таблицу!\n👉 {KPI_LINK}")
    else:
        await update.message.reply_text("Пожалуйста, выбери команду с кнопки ниже 👇")

# Нагадування 1-го числа
async def monthly_reminder_kpi(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "📅 *Пора поставить KPI на месяц!*\n"
            "Дедлайн — *2-е число* каждого месяца.\n"
            "Пожалуйста, внесите задачи в таблицу:\n"
            f"{KPI_LINK}\n\n"
            "⚠️ Обратите внимание: все задачи должны быть открыты *для Светланы Красниковой*, "
            "а также Никиты Филимонова, Ольги Мец и Марины."
        ),
        parse_mode='Markdown'
    )

# Нагадування 28-го числа
async def kpi_completion_reminder(context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=CHAT_ID,
        text=(
            "📌 *Финальный штрих!* Приближается дедлайн по KPI.\n"
            "Просим внести выполнение KPI в таблицу до конца завтрашнего дня:\n"
            f"{KPI_LINK}"
        ),
        parse_mode='Markdown'
    )

# Ініціалізація застосунку
app = ApplicationBuilder().token(TOKEN).build()

# Обробники команд
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# ПЛАНУВАЛЬНИК (apscheduler)
scheduler = BackgroundScheduler(timezone="Europe/Kyiv")

# 1-е число щомісяця, 10:00
scheduler.add_job(
    monthly_reminder_kpi,
    trigger='cron',
    day=1,
    hour=10,
    minute=0,
    args=[app.bot]
)

# 28-е число щомісяця, 10:00
scheduler.add_job(
    kpi_completion_reminder,
    trigger='cron',
    day=28,
    hour=10,
    minute=0,
    args=[app.bot]
)

scheduler.start()
app.run_polling()
