# Основной файл, где будет проходить главный поток программы
from pathlib import Path

import telebot
from telebot import types
import database
import userInteraction
import base64

# в файле database будут храниться все методы для взаимодействия с бд

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

# данные пользователя
UserID = 0
UserName = ''
Age = 0
GenderID = 0
City = ''
MaleSearchID = 0
UserDescription = ''
PhotoCount = 0


@bot.message_handler(commands='start')
def start_message(message):
    global UserID
    UserID = message.from_user.id

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
    database.db_user_val(UserID, UserName, Age, GenderID, City, MaleSearchID, UserDescription)

    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Сохранить'))

    msg = bot.send_message(message.chat.id,
                           'Выбери свои предпочтения в еде, написав соответсвующие цифры в чат, как закончишь нажми на кнопку:\n\n'
                           '1 - Фастфуд\n'
                           '2 - Китайская кухня\n'
                           '3 - Японская кухня\n'
                           '4 - Грузинская кухня\n'
                           '5 - Итальянаская кухня\n', reply_markup=rmk)

    bot.register_next_step_handler(msg, get_userFood)


def get_userFood(message):
    if message.text == 'Сохранить':
        get_firstPhoto(message)
    else:
        try:
            int(message.text)
        except ValueError:
            msg = bot.send_message(message.chat.id, 'Можно вводить только цифры!\nПопробуйте еще раз:')
            bot.register_next_step_handler(msg, get_userFood)

        if int(message.text) > 5 or int(message.text) <= 0:
            msg = bot.send_message(message.chat.id,
                                   'Значение должно быть больше 0 и меньше или равно 5!\nПопробуйте еще раз:')
            bot.register_next_step_handler(msg, get_userFood)
        else:
            database.db_prefer_val(UserID, message.text, message)
            msg = bot.send_message(message.chat.id, 'Продолжайте!\nЕсли хотите закончить нажмите на кнопку:')
            bot.register_next_step_handler(msg, get_userFood)


def get_firstPhoto(message):
    rmk = types.ReplyKeyboardRemove()

    msg = bot.send_message(message.chat.id, 'Остался последний шаг! Отправьте до 3-х фотографий:', reply_markup=rmk)
    bot.register_next_step_handler(msg, get_photo)


def get_photo(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Сохранить'))
    global PhotoCount

    if message.text == 'Сохранить':
        if PhotoCount != 0:
            final(message)
        else:
            msg = bot.send_message(message.chat.id, 'Вы не добавили ни одной фотографии!\nМы не можем продолжить, пока вы не добавите хотя бы 1 фото', reply_markup=rmk)
            bot.register_next_step_handler(msg, get_photo)
    elif message.content_type == 'photo':
        messageLength = message[-1].message_id - message.message_id

        if messageLength > 3:
            msg = bot.send_message(message.chat.id, 'Нельзя добавлять больше 3-х фото!\n Повторите попытку либо сохраните результат', reply_markup=rmk)
            bot.register_next_step_handler(msg, get_photo)
        elif messageLength > (3 - PhotoCount):
            msg = bot.send_message(message.chat.id, f'Вы можете добавить еще {3 - PhotoCount}!\n Повторите попытку либо сохраните результат.', reply_markup=rmk)
            bot.register_next_step_handler(msg, get_photo)
        elif messageLength > 1:
            PhotoCount += message[-1].message_id - message.message_id
            print('соси')
#           for c in message.photo:
#              src = database.save_photo(c)
#             database.insert_blob(UserID, src)

            if PhotoCount < 3:
                msg = bot.send_message(message.chat.id, f'Отлично! Отправлено {PhotoCount} из 3 фото\nЕсли хотите закончить нажмите на кнопку', reply_markup=rmk)
                bot.register_next_step_handler(msg, get_photo)
            else:
                bot.send_message(message.chat.id, 'Отлично! Все фото добавлены, перейдем далее')
                final(message)
        else:
            src = database.save_photo(message)
            database.insert_blob(UserID, src)
            PhotoCount += 1

            if PhotoCount < 3:
                msg = bot.send_message(message.chat.id, f'Отлично! Отправлено {PhotoCount} из 3 фото\nЕсли хотите закончить нажмите на кнопку', reply_markup=rmk)
                bot.register_next_step_handler(msg, get_photo)
            else:
                bot.send_message(message.chat.id, 'Отлично! Все фото добавлены, перейдем далее')
                final(message)
    else:
        bot.reply_to(message, "Можно отправлять только фотографии!\n(Когда выбираете фото поставьте галочку напротив \'Сжать изображение\')")
        msg = bot.send_message(message.chat.id, 'Попробуйте еще раз!', reply_markup=rmk)
        bot.register_next_step_handler(msg, get_photo)


def final(message):
    bot.send_message(message.chat.id, 'suck my nuts')


@bot.message_handler(commands='menu')
def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('👤 Изменить пользователя')
    item2 = types.KeyboardButton('🔍 Поиск')

    markup.add(item1, item2)
    msg = bot.send_message(message.chat.id, 'Выбери, что тебя интересует', reply_markup=markup)
    bot.register_next_step_handler(msg, menu_choice)


def menu_choice(message):
    if message.text == '👤 Изменить пользователя':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('👤 Имя')
        item2 = types.KeyboardButton('👤 Возраст')
        item3 = types.KeyboardButton('👤 Пол')
        item4 = types.KeyboardButton('👤 Город')
        item5 = types.KeyboardButton('👤 Описание')
        item6 = types.KeyboardButton('👤 Предпочтения в еде')
        markup.add(item1, item2, item3, item4, item5, item6)
        msg = bot.send_message(message.chat.id, 'Что хочешь изменить?', reply_markup=markup)
        bot.register_next_step_handler(msg, change_UserSettings)
    elif message.text == '🔍 Поиск':
        print()


def change_UserSettings(message):
    if message.text == '👤 Имя':
        welcome(message)
    elif message.text == '👤 Имя':
        welcome(message)
    elif message.text == '👤 Имя':
        welcome(message)
    elif message.text == '👤 Имя':
        welcome(message)
    elif message.text == '👤 Имя':
        welcome(message)
    elif message.text == '👤 Имя':
        welcome(message)


bot.infinity_polling()
