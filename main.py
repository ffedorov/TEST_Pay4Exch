import os
import telebot
import logging
import psycopg2

from config import *
from flask import Flask, request
from datetime import datetime

from telebot import types
import requests
import json

bot = telebot.TeleBot(BOT_TOKEN)
server = Flask(__name__)
logger = telebot.logger
logger.setLevel(logging.DEBUG)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_oject = db_connection.cursor()

@bot.message_handler(commands=["start"])
def start(message):
    id = message.from_user.id
    username = message.from_user.username
    bot.reply_to(message, f"Hello, {username}!\nWe are checking your details...")

    db_oject.execute(f"SELECT id FROM users WHERE id = {id}")
    result = db_oject.fetchone()

    if not result:
        db_oject.execute("INSERT INTO users(id, username, usercontact) VALUES (%s, %s, %s)", (id, username, ''))
        db_connection.commit()
        bot.send_message(id, f"You are identified.\nAll is ready.")
    else:
        bot.send_message(id, f"Identification is not required.\nYou have already been identified.")

# ##########################################------------------------

@bot.message_handler(commands=["docnum"])
def docnum(message):

    doc_id = datetime.utcnow()
    bot.reply_to(message, ("Номер документа: " + str(doc_id)))

# ##########################################------------------------

@bot.message_handler(commands=["pay"]) # Формирование онлайн оплаты
def pay(message):

#    doc_id = datetime.utcnow()
#    id = message.from_user.id

    bot.register_next_step_handler(bot.send_message(message.chat.id, 'Укажите номер заявки:'), NUMBER = message.text)
    bot.register_next_step_handler(bot.send_message(message.chat.id, f"Укажите сумму для оплаты заявки: {NUMBER}"),  SUMM = message.text)
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(
    types.InlineKeyboardButton(text='Да', callback_data='Да'),
    types.InlineKeyboardButton(text='Нет', callback_data='Нет')
    )
    bot.register_next_step_handler(
        bot.send_message(message.from_user.id, f"Сформировать ссылку для онлайн оплаты заявки {SUMM} на сумму {SUMM} ?",
                         reply_markup=keyboard)
    )
    if message.text == 'Да':
#        Генерируем ссылку TKB-Pay
        bot.send_message(message.chat.id, f"Ссылка для оплаты картой:\nHttps://www.google.com")
    elif message.text == 'Нет':
        bot.send_message(message.chat.id, 'Отмена.')
    else:
        bot.send_message(message.chat.id, 'Необходимо выбрать.')

#

# Ждём номер заявки и записываем в number
# Ждём сумму заявки и записываем в summ
# Кнопки подтверждения и отмемы
# При отмене повтор, при подтверждении генерим ссылку

#    bot.send_message(id, f"Ссылка для оплаты картой:\nHttps://www.google.com")





# /api/v1/card/unregistered/debit

# {
#  "ExtID":"ID88618_176418_test8",
#  "Amount":600000,
#  "Description":"Оплата по договору 123_test Иванова И.И.",
#  "ReturnURL":"http://site.ru_result",
#  "ClientInfo": {
#                 "Email":"test@test.com",
#                 "PhoneNumber": "+7 (911) 123-00-00"
#                },
#  "TTL":"4.00:00:00",
#  "CartPositions":[{
#                   "Quantity":1.0,
#                   "Price":300000,
#                   "Tax":60,
#                   "Text":"Оплата по договору 123_test Иванова И.И.",
#                   "PaymentMethodType":4,
#                   "PaymentSubjectType":4
#                   }],
#  "AdditionalParameters":{
#                         "DogovorID":"12345_test"
#                         }
# }















# ##########################################------------------------

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
