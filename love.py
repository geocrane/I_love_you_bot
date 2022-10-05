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

MESSAGES = {
    "first": "Сережа просил передать, что ты у него {compliment_1} и {compliment_2}.",
    "second": "Твой муж мне сказал, что он тебя любит, потому что ты {compliment_1} и {compliment_2}.",
    "third": "А тебе кто-нибудь говорил, что ты {compliment_1} и {compliment_2}?",
    "forth": "Исключительно от себя скажу, что ты {compliment_1} и {compliment_2}.",
    "fifth": "По секрету, любой мужчина должен видеть, какая ты {compliment_1} и {compliment_2}",
    "six": "Разве есть еще женщина более {compliment_1} и {compliment_2}, чем ты?",
    "seven": "Сережа счастлив, что у него такая {compliment_1} и {compliment_2} жена."
}


def get_compliments():
    list_index = ["first", "second", "third", "forth", "fifth", "six", "seven"]
    index_0 = random.randrange(0, (len(list_index)-1))
    message = MESSAGES.get(list_index[index_0])
    index_1 = random.randrange(1, (len(compliments) - 1))
    compliment_1 = compliments.get(index_1)
    index_2 = random.randrange(1, len(compliments))
    if index_2 == index_1:
        index_2 += 1
    compliment_2 = compliments.get(index_2)
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
