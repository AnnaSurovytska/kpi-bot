import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from apscheduler.schedulers.background import BackgroundScheduler

TOKEN = os.getenv("TOKEN")

# Завантаження chat_id з файлу (або створюється після /getchatid)
CHAT_ID = None
try:
    with open("chat_id.txt", "r") as f:
        CHAT_ID = f.read().strip()
except FileNotFoundError:
    print("Файл chat_id.txt не знайдено — буде створено після команди /getchatid")

KPI_LINK = 'https://docs.google.com/spreadsheets/d/187czH5iolCe_wmARbZ_blpQjzJQHQ7__/edit?gid=1652687997'

KPI_INFO = {
    "Что такое KPI": (
        "📊 *KPI* — это конкретная метрика или задача, по которой оценивают, "
        "насколько хорошо ты справляешься со своей работой.\n\n"
        "💡 Или, как сказал *Питер Друкер*: _«То, что измеряется — улучшается»_."
    ),
    "Инструкция": (
        "✍️ Пишем задачи по *SMART*: конкретны, измеримы, достижимы, релевантны, ограничены по времени.\n\n"
        "📌 *1) Фокусные задачи:*\n"
        "Каждый месяц у тебя и сотрудников должны быть задачи в *Asana*, привязанные к KPI.\n\n"
        "📌 *2) Постановка задач:*\n"
        "С 1 по 3 число ставим задачи и вносим в таблицу.\n\n"
        "📌 *3) Отчет:*\n"
        "До 30 числа — заполняем таблицу: ссылка, %, и качество выполнения."
    ),
    "Критерии": (
        "✅ Задача считается выполненной, если:\n"
        "• выполнена на *100%*\n"
        "• в срок\n"
        "• и с нужным качеством ✅"
    )
}

keyboard = [
    ["Что такое KPI", "Инструкция"],
    ["Критерии", "Файл"]
]
markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я помогу тебе не забыть про KPI и подскажу, как правильно их оформить.",
        reply_markup=markup
    )

# Обработка кнопок
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text in KPI_INFO:
        await update.message.reply_text(KPI_INFO[text], parse_mode='Markdown')
    elif text == "Файл":
        await update.message.reply_text(f"📎 Вот таблица KPI:\n{KPI_LINK}")
    else:
        await update.message.reply_text("Пожалуйста, выбери команду с кнопки ниже 👇")

# /getchatid
async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None or update.message.chat.type not in ['group', 'supergroup', 'private']:
        return

    global CHAT_ID
    CHAT_ID = str(update.effective_chat.id)

    with open("chat_id.txt", "w") as f:
        f.write(CHAT_ID)

    await update.message.reply_text(
        f"✅ Ваш chat_id сохранён: `{CHAT_ID}`",
        parse_mode="Markdown"
    )

# Напоминание 1-го числа
async def monthly_reminder_kpi(context: ContextTypes.DEFAULT_TYPE):
    if CHAT_ID:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=(
                "📅 *Пора поставить KPI на месяц!*\n"
                "Дедлайн — *2-е число* каждого месяца.\n"
                "Пожалуйста, внесите задачи в таблицу:\n"
                f"{KPI_LINK}\n\n"
                "⚠️ Все задачи должны быть открыты *для Светланы Красниковой*, "
                "а также Никиты Филимонова, Ольги Мец и Марины."
            ),
            parse_mode='Markdown'
        )

# Напоминание 28-го числа
async def kpi_completion_reminder(context: ContextTypes.DEFAULT_TYPE):
    if CHAT_ID:
        await context.bot.send_message(
            chat_id=CHAT_ID,
            text=(
                "📌 *Финальный штрих!* Приближается дедлайн по KPI.\n"
                "Просим внести выполнение KPI в таблицу до конца завтрашнего дня:\n"
                f"{KPI_LINK}"
            ),
            parse_mode='Markdown'
        )

# Запуск
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("getchatid", get_chat_id))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# Планировщик
scheduler = BackgroundScheduler(timezone="Europe/Kyiv")
scheduler.add_job(monthly_reminder_kpi, trigger='cron', day=1, hour=10, minute=0, args=[app.bot])
scheduler.add_job(kpi_completion_reminder, trigger='cron', day=28, hour=10, minute=0, args=[app.bot])
scheduler.start()

app.run_polling()
