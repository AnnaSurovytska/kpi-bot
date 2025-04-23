from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import datetime

# ВСТАВЬ сюда свой токен от BotFather
TOKEN = '7523350616:AAGIflsN_BP3tK2Kehoh7_8yNS7BZSMs-8E '

# Ссылка на Google таблицу с KPI
KPI_LINK = 'https://docs.google.com/spreadsheets/d/187czH5iolCe_wmARbZ_blpQjzJQHQ7__/edit?gid=1652687997'

# Справочная информация
KPI_INFO = {
    "что_такое_kpi": "KPI — это ваши ключевые показатели эффективности. Они показывают, насколько успешно человек или команда достигает целей.",
    "как_писать": "Формулируйте задачи по принципу SMART: конкретно, измеримо, достижимо, релевантно, ограничено по времени.",
    "критерии": "Задача считается выполненной, если она выполнена на 100%, в срок и с нужным качеством."
}

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я помогу тебе не забыть про KPI и подскажу, как правильно их оформлять.")

# Информационные команды
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    команда = update.message.text.replace("/", "")
    if команда in KPI_INFO:
        await update.message.reply_text(KPI_INFO[команда])
    else:
        await update.message.reply_text("Команда не найдена. Попробуй /что_такое_kpi, /как_писать или /критерии")

# Напоминание по датам
async def напоминание(update: Update, context: ContextTypes.DEFAULT_TYPE):
    сегодня = datetime.date.today()
    if 1 <= сегодня.day <= 3:
        текст = f"🗓 Время поставить KPI-задачи на месяц!\n👉 Таблица: {KPI_LINK}"
    elif 28 <= сегодня.day <= 30:
        текст = f"📊 Пора обновить статус задач по KPI!\n👉 Таблица: {KPI_LINK}"
    else:
        текст = "Сегодня нет задач по KPI. Наслаждайся 😉"
    await update.message.reply_text(текст)

# Запуск бота
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("что_такое_kpi", info))
app.add_handler(CommandHandler("как_писать", info))
app.add_handler(CommandHandler("критерии", info))
app.add_handler(CommandHandler("напоминание", напоминание))

app.run_polling()
