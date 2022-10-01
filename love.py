import os
import random
import time

from telegram import ReplyKeyboardMarkup, Bot
from telegram.ext import CommandHandler, Updater
from dotenv import load_dotenv

from compliments import compliments

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def get_compliments():
    index = random.randrange(1, 100)
    compliment_1 = compliments.get(index)
    index = random.randrange(1, 100)
    compliment_2 = compliments.get(index)
    return (
        f"Сережа просил передать, что ты у него "
        f"{compliment_1} и {compliment_2}"
    )


def new_compliment(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat.id, get_compliments())


def wake_up(update, context):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup([["/compliment"]], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=(
            "Привет, Викуля. Твой муж тебя очень любит "
            "и хочет сказать тебе много слов."
        ),
        reply_markup=button,
    )

    context.bot.send_message(chat.id, get_compliments())


def main():
    updater = Updater(token=TELEGRAM_TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(
        CommandHandler("compliment", new_compliment)
    )
    while True:
        updater.start_polling()
        # updater.idle()
        bot = Bot(token=TELEGRAM_TOKEN)
        message = get_compliments()
        bot.send_message(TELEGRAM_CHAT_ID, message)
        time.sleep(600)


if __name__ == "__main__":
    main()
