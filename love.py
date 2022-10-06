import os
import random
import time

from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from compliments import COMPLIMENTS
from messages import MESSAGES

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def get_endings(compliment, ending):
    return compliment + ending


def get_compliments():
    index_0 = random.randrange(0, (len(MESSAGES) - 1))
    message = MESSAGES[index_0]
    index_1 = random.randrange(0, (len(COMPLIMENTS) - 2))
    compliment_1 = COMPLIMENTS[index_1]
    index_2 = random.randrange(0, (len(COMPLIMENTS) - 1))
    if index_2 == index_1:
        index_2 += 1
    compliment_2 = COMPLIMENTS[index_2]
    return message.format(compliment_1=compliment_1, compliment_2=compliment_2)


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
        bot = Bot(token=TELEGRAM_TOKEN)
        message = get_compliments()
        bot.send_message(TELEGRAM_CHAT_ID, message)
        time.sleep(7200)


if __name__ == "__main__":

    main()
