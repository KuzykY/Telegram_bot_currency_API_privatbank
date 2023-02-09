import os

import telebot
import requests
from telebot import types
from dotenv import load_dotenv

load_dotenv()

API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

response = requests.get('https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11').json()


@bot.message_handler(commands=['start'])
def menu(message):
    greeting = f'Hi, {message.from_user.first_name} , I am Currency Bot. Make your choice!'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('USD')
    btn2 = types.KeyboardButton('EUR')
    keyboard.add(btn1, btn2)
    msg = bot.send_message(message.chat.id, greeting, reply_markup=keyboard)
    bot.register_next_step_handler(msg, coin_step)


def coin_step(message):
    try:
        keyboard = types.ReplyKeyboardRemove(selective=False)

        for coin in response:
            if message.text == coin['ccy']:
                bot.send_message(message.chat.id, printCoin(coin['buy'], coin['sale']), reply_markup=keyboard)

    except Exception as e:
        bot.reply_to(message, 'oopss')


def printCoin(buy, sale):
    return 'Курс покупки: ' + str(buy) + '\n Курс Продажу:' + str(sale)


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

if __name__ == '__main__':
    bot.polling(none_stop=True)
