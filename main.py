import os
import telebot
import logging
from config import *
from flask import Flask, request
from datetime import datetime

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=["start"])
def start(message):
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!")

# ------------------------

@bot.message_handler(commands=["docnum"])
def docnum(message):

    DOC_ID = datetime.utcnow()
    bot.reply_to(message, ("Номер документа: " + str(DOC_ID)))
    # bot.send_message(message.chat.id, ('Номер документа: ' + str(Doc_id))) # Текст Telegram



# ------------------------

@server.route(f"/{BOT_TOKEN}", methods=["POST"])
def redirect_message():
    json_string = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=APP_URL)
    server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
