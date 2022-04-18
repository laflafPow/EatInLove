# В этом файле будут храниться методы взаимодействия с пользователем

import telebot
from telebot import types
import database

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

def start_message(message):
    msg = bot.send_message(message.chat.id, 'Привет! Я помогу найти'
                                            ' тебе человека с которым '
                                            'ты сможешь хорошо провести время,'
                                            ' т.е. покушать, но для начала'
                                            ' расскажи чутка о себе,'
                                            ' чтобы я нашел подходящего человека...'
                                            '\n\nКак тебя зовут?')
    bot.register_next_step_handler(msg, get_age)


def get_age(message):
    msg = bot.send_message(message.chat.id, 'Крутое имя, перейдем дальше, сколько тебе лет?')

    bot.register_next_step_handler(msg, get_gender)


def get_gender(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Мужской'), types.KeyboardButton('Женский'))

    msg = bot.send_message(message.chat.id, 'Укажи свой пол', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_genderSearch)


def get_genderSearch(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Мужчин'), types.KeyboardButton('Женщин'), types.KeyboardButton('Всех'))

    msg = bot.send_message(message.chat.id, 'Кого будем искать?', reply_markup=rmk)