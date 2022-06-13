# Основной файл, где будет проходить главный поток программы

import telebot
from telebot import types
import database
import userInteraction

# в файле database будут храниться все методы для взаимодействия с бд

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

# данные пользователя
UserName = ''
Age = 0
GenderID = 0
City = ''
MaleSearchID = 0
UserDescription = ''


@bot.message_handler(commands='start')
def start_message(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('ОК'))

    bot.send_message(message.chat.id, 'Привет! Я помогу найти'
                                      ' тебе человека с которым '
                                      'ты сможешь хорошо провести время,'
                                      ' т.е. покушать, но для начала'
                                      ' расскажи чутка о себе,'
                                      ' чтобы я нашел подходящего человека...', reply_markup=rmk)

    bot.register_next_step_handler(message, welcome)

def welcome(message):
    rmk = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, 'Как тебя зовут?', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_Name)

def get_Name(message):
    global UserName
    UserName = message.text
    msg = bot.send_message(message.chat.id, 'Крутое имя, перейдем дальше, сколько тебе лет?')
    bot.register_next_step_handler(msg, get_Age)

def get_Age(message):
    global Age
    while Age == 0:  # проверяем что возраст изменился
        try:
            Age = int(message.text)  # проверяем, что возраст введен корректно
        except ValueError:
            bot.send_message(message.from_user.id, 'Цифрами, пожалуйста')

    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Мужской'), types.KeyboardButton('Женский'))

    msg = bot.send_message(message.chat.id, 'Укажи свой пол', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_Gender)

def get_Gender(message):
    global GenderID
    while GenderID == 0:
        if message.text == 'Мужской':
            GenderID = 2
        elif message.text == 'Женский':
            GenderID = 1
        else:
            bot.send_message(message.from_user.id, 'Пол введен некорректно')

    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Мужчин'), types.KeyboardButton('Женщин'), types.KeyboardButton('Всех'))

    msg = bot.send_message(message.chat.id, 'Кого будем искать?', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_MaleSearch)


def get_MaleSearch(message):
    global MaleSearchID
    while MaleSearchID == 0:
        if message.text == 'Мужчин':
            MaleSearchID = 2
        elif message.text == 'Женщин':
            MaleSearchID = 1
        elif message.text == 'Всех':
            MaleSearchID = 3
        else:
            bot.send_message(message.from_user.id, 'Введено некорректное значение')

    rmk = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, 'Укажите город!', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_City)

def get_City(message):
    global City
    while City == '':
        try:
            int(message.text)
            bot.send_message(message.chat.id, 'Некорректное значение')
        except ValueError:
            try:
                City = str(message.text)
            except ValueError:
                bot.send_message(message.chat.id, 'Некорректное значение')

    msg = bot.send_message(message.chat.id, 'Расскажи что-то о себе. Это повысит шанс на взаимную симпатию:)')
    bot.register_next_step_handler(msg, get_userDescription)

def get_userDescription(message):
    global UserDescription
    UserDescription = message.text
    database.db_user_val(UserName, Age, GenderID, City, MaleSearchID, UserDescription)

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