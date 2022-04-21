# Основной файл, где будет проходить главный поток программы

import telebot
from telebot import types
import database
import userInteraction

# в файле database будут храниться все методы для взаимодействия с бд

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

@bot.message_handler(commands='start')
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

    bot.register_next_step_handler(msg, get_city)


def get_city(message):
    rmk = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, 'Укажите город!', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_userDescription)

def get_userDescription(message):
    msg = bot.send_message(message.chat.id, 'Расскажи что-то о себе. Это повысит шанс на взаимную симпатию:)')
    bot.register_next_step_handler(msg, get_userPrefer)

def get_userPrefer(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Сохранить'))

    msg = bot.send_message(message.chat.id, 'Выбери свои предпочтения в еде нажав на соответсвующие цифры, как закончишь нажми на кнопку:\n\n'
                                            '/1 - Фастфуд\n'
                                            '/2 - Китайская кухня\n'
                                            '/3 - Японская кухня\n'
                                            '/4 - Грузинская кухня\n'
                                            '/5 - Итальянаская кухня\n',
                                            reply_markup=rmk)

    bot.register_next_step_handler(msg, get_photo)

@bot.message_handler(content_types= ['photo'])
def get_photo(message):
    rmk = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, 'Остался последний шаг! Отправьте до 3-х фотографий:', reply_markup=rmk)

bot.infinity_polling()