import os
import telebot
import logging
from config import *
from flask import Flask, request


bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)


@bot.message_handler(commands=["start"])
def start(message):
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!")

#------------------------

@bot.message_handler(commands=['docnum'])
def docnum(message):
    # Таблица транзакций ###################################################################################################

    # connect = sqlite3.connect('Payments.db')
    # cursor = connect.cursor()
    # cursor.execute("""CREATE TABLE IF NOT EXISTS telegram_id(
      #      id INTEGER,
      #      summ FLOAT,
      #      name INTEGER
      #  )""")

    # connect.commit()

    Doc_id = datetime.utcnow()
    bot.reply_to(message, 'Номер документа: ' + str(Doc_id))
    # bot.send_message(message.chat.id, ('Номер документа: ' + str(Doc_id))) # Текст Telegram

    #summ = 123.9501
    #new_str = [Doc_id, summ, message.chat.id]  # список записей пользователя
    #cursor.execute("INSERT INTO telegram_id VALUES(?,?,?);", new_str)
    #connect.commit()

#------------------------

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
