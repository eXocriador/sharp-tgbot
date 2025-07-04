import logging
import random
import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes,
    MessageHandler, filters
)

logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__), 'bot.log'),
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

PREDICTIONS = [
    "Да",
    "Нет",
    "Возможно",
    "Скорее всего да",
    "Скорее всего нет",
    "Спроси позже",
    "Без сомнений",
    "Не могу сейчас сказать",
    "Определённо да",
    "Определённо нет",
    "Ты серьёзно это спрашиваешь?",
    "Ты чё, еблан?",
    "Даже шар не знает, что ты несёшь",
    "Лучше иди поешь",
    "Сначала допей кофе, потом спроси",
    "Да, но это не точно",
    "Нет, но ты всё равно сделаешь по-своему",
    "Дружище, ну тут всё понятно без меня",
    "Ой, отстань, дай поспать",
    "Не сейчас, я занят мемами",
    "Скорее всего да, но лучше проверь дважды",
    "Вангую провал",
    "Звучит как проблема будущего тебя",
    "Надейся и жди",
    "Конечно... нет",
    "Шансов больше, чем у тебя на сессию",
    "Это фиаско, братан",
    "Да, но только в параллельной вселенной",
    "Ха-ха, нет",
    "Да, но потом ты об этом пожалеешь",
    "Астрологи объявили неделю хуйни. Твоя очередь",
    "Слишком тупой вопрос даже для шара",
    "Ну ты и клоун, конечно"
]

RANDOM_STICKERS = [
    "CAACAgIAAxkBAhbT0WhoCXTfIA47Z1WFGdgQzxxkpXcvAAJebgAC1AZoSpj0wnjrf1AgNgQ",
    "CAACAgIAAxkBAhbTzmhoCWtc_1OXgDXcDz0BI4iM4ekDAAI7ZQAC2aJpSrSCDWePPkUhNgQ",
    "CAACAgIAAxkBAhbTymhoCWW3kVtJgBuY5oXZCxTcX-_eAALIkQACNZJpSiyGErkrKfisNgQ",
    "CAACAgIAAxkBAhbTyGhoCV9EJrUENLRR4mPY35oenHSmAAJNYgACWgVpSg-NmLJJRhgzNgQ",
    "CAACAgIAAxkBAhbTxWhoCVcwCkdDSafpvWgmoR_WpTY1AAIuZQAClIlpSqjkbUVPUXPMNgQ",
    "CAACAgIAAxkBAhbTwmhoCVHEOfYzJ2_TVl4pM05KanSsAAIzdAACdedpSrbRUzI__1QWNgQ",
    "CAACAgIAAxkBAhbTwGhoCUTbI2JFW5HG2tPkmd6sjtORAAJkdAAC4OJgSrC5eX93kQABiTYE",
    "CAACAgIAAxkBAhbTu2hoCTuEewrhDcsDqhb037M5DYMXAAIjbgACaytoSgeuiyXIVFofNgQ",
    "CAACAgIAAxkBAhbTt2hoCTAgos2tSbFBbInyR0kAAVpSwwAC1nUAAt8qYEoVcMOHXNnz_jYE",
    "CAACAgIAAxkBAhbTtGhoCSheXwzzv5PUmWgKp9ve_qO2AAIpZAAC6shoSvg7lenjt34MNgQ"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Привет! Я SHARP мемный бот.\n\n"
        "🔮 Напиши свой вопрос, и я выдам тебе предсказание с мемным стикером.\n\n"
        "Для помощи введи /help"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📝 *Инструкция*\n\n"
        "1️⃣ В группе — отвечаю, если меня упомянули (тегнули).\n"
        "2️⃣ В личке — отвечаю на любые сообщения.\n"
        "3️⃣ Получи SHARP предсказание + мемный стикер.\n\n"
        "✨ *Новые фичи*: токсичные предсказания и рандомные стикеры.\n\n"
        "⚠️ Внимание: вопросы логируются без текста, для улучшения бота."
        , parse_mode="Markdown"
    )

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    user = message.from_user
    bot_username = (await context.bot.get_me()).username.lower()

    # Проверяем, где сообщение
    if message.chat.type in ["group", "supergroup"]:
        # Ищем упоминание бота
        if not message.entities:
            return  # без упоминаний молчим

        mention_found = False
        for entity in message.entities:
            if entity.type == "mention":
                mention_text = message.text[entity.offset : entity.offset + entity.length].lower()
                if mention_text == f"@{bot_username}":
                    mention_found = True
                    break
        if not mention_found:
            return  # без упоминания — молчим

        # Убираем упоминание из текста, чтобы получить вопрос
        question = message.text.replace(f"@{bot_username}", "").strip()
        if not question:
            await message.reply_text("❗ Задай вопрос после упоминания меня!")
            return
    else:
        # Личная переписка — любой текст = вопрос
        question = message.text

    prediction = random.choice(PREDICTIONS)
    sticker_id = random.choice(RANDOM_STICKERS)

    logging.info(f"User: {user.username or user.first_name} | Chat: {message.chat.id} | Prediction sent")

    await message.reply_text(f"🔮 *Предсказание*: {prediction}", parse_mode="Markdown")
    await message.reply_sticker(sticker_id)


def main():
    TOKEN = "ВАШ_ТОКЕН"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, predict))

    print("🤖 SHARP MEME BOT запущен!")
    app.run_polling()


if __name__ == "__main__":
    main()
