import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

TOKEN = os.getenv("TOKEN")
KPI_LINK = 'https://docs.google.com/spreadsheets/d/187czH5iolCe_wmARbZ_blpQjzJQHQ7__/edit?gid=1652687997'

CHAT_ID = None
try:
    with open("chat_id.txt", "r") as f:
        CHAT_ID = f.read().strip()
except FileNotFoundError:
    print("Файл chat_id.txt не найден. Он будет создан при первом использовании /getchatid.")

# --- KPI информация с экранированным MarkdownV2 ---
KPI_INFO = {
    "Что такое KPI": (
        "📊 *KPI* — это конкретная метрика или задача, по которой оценивают, "
        "насколько хорошо ты справляешься со своей работой\\.\n\n"
        "💡 Как сказал Питер Друкер: _«То, что измеряется — улучшается»_\\."
    ),
    "Инструкция": (
        "✍️ Пишем задачи по *SMART*: \n"
        "\\- конкретны\n"
        "\\- измеримы\n"
        "\\- достижимы\n"
        "\\- релевантны\n"
        "\\- ограничены по времени\n\n"
        "📌 *1\\) Фокусные задачи:* должны быть в Asana и связаны с KPI\\.\n"
        "📌 *2\\) Ставим задачи с 1 по 3 число и вносим в таблицу\\.\n"
        "📌 *3\\) До 30 числа — отчёт: статус, ссылка, качество\\."
    ),
    "Критерии": (
        "✅ Задача считается выполненной, если:\n"
        "\\- выполнена на *100%*\n"
        "\\- в срок\n"
        "\\- и с нужным качеством ✅"
    )
}

# --- Клавиатура ---
keyboard = [
    ["Что такое KPI", "Инструкция"],
    ["Критерии", "Файл"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# --- Команды ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет\\! Я помогу тебе не забыть про KPI и подскажу, как правильно их оформить\\.",
        reply_markup=markup,
        parse_mode='MarkdownV2'
    )

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CHAT_ID
    CHAT_ID = str(update.effective_chat.id)
    with open("chat_id.txt", "w") as f:
        f.write(CHAT_ID)
    await update.message.reply_text(
        f"✅ Ваш chat\\_id сохранён: `{CHAT_ID}`", parse_mode="MarkdownV2"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        print(f"[DEBUG] Получено сообщение: {text}")

        if text in KPI_INFO:
            await update.message.reply_text(KPI_INFO[text], parse_mode='MarkdownV2')
        elif text == "Файл":
            await update.message.reply_text(f"📎 Вот таблица KPI:\n{KPI_LINK}")
        else:
            await update.message.reply_text("Пожалуйста, выбери команду с кнопки ниже 👇")

    except Exception as e:
        print(f"[ERROR] Ошибка в handle_message: {e}")
        await update.message.reply_text("⚠️ Что-то пошло не так при обработке команды.")

# --- Напоминания ---
async def monthly_reminder_kpi(context: ContextTypes.DEFAULT_TYPE):
    if CHAT_ID:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=(
                "📅 *Пора поставить KPI на месяц\\!*\\n"
                "Дедлайн — *2\\-е число* каждого месяца\\.\n\n"
                "📝 Пожалуйста, внесите задачи в таблицу:\n"
                f"{KPI_LINK}\n\n"
                "⚠️ Все задачи должны быть открыты *для Светланы Красниковой*, "
                "а также *Никиты Филимонова*, *Ольги Мец* и *Марины*\\."
            ),
            parse_mode='MarkdownV2'
        )

async def kpi_completion_reminder(context: ContextTypes.DEFAULT_TYPE):
    if CHAT_ID:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=(
                "📌 *Финальный штрих\\!* Приближается дедлайн по KPI\\.\n"
                f"Заполните таблицу до конца завтрашнего дня:\n{KPI_LINK}"
            ),
            parse_mode='MarkdownV2'
        )

# --- Инициализация ---
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("getchatid", get_chat_id))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    scheduler = BackgroundScheduler(timezone="Europe/Kyiv")
    scheduler.add_job(monthly_reminder_kpi, 'cron', day=1, hour=10, args=[app.bot])
    scheduler.add_job(kpi_completion_reminder, 'cron', day=28, hour=10, args=[app.bot])

    # Тестовое напоминание через 10 секунд после старта
    scheduler.add_job(monthly_reminder_kpi, 'date', run_date=datetime.now() + timedelta(seconds=10), args=[app.bot])

    scheduler.start()
    app.run_polling()
