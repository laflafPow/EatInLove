# Основной файл, где будет проходить главный поток программы
import sqlite3
from pathlib import Path

import telebot
from telebot import types
import database
import userInteraction
import base64

# в файле database будут храниться все методы для взаимодействия с бд

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)


conn = sqlite3.connect('db/UserDatabase.db', check_same_thread=False)
cursor = conn.cursor()


# данные пользователя
UserName = ''
Age = 0
GenderID = 0
City = ''
MaleSearchID = 0
UserDescription = ''
PhotoCount = 0


@bot.message_handler(commands='start')
def start_message(message):
    cursor.execute(
        'INSERT INTO User (UserID, ChatID) VALUES (?, ?)',
        (message.from_user.id, message.chat.id))
    conn.commit()

    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('ОК👌'))

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
    database.db_changeName(message.from_user.id, message.text)
    msg = bot.send_message(message.chat.id, 'Крутое имя, перейдем дальше, сколько тебе лет?')
    bot.register_next_step_handler(msg, get_Age)


def get_Age(message):
    if int(message.text):
        if 100 >= int(message.text) > 0:
            database.db_changeAge(message.from_user.id, int(message.text))
            rmk = types.ReplyKeyboardMarkup()
            rmk.add(types.KeyboardButton('Мужской'), types.KeyboardButton('Женский'))

            msg = bot.send_message(message.chat.id, 'Отлично, укажи пол', reply_markup=rmk)
            bot.register_next_step_handler(msg, get_Gender)
        else:
            bot.send_message(message.chat.id, 'Введенено неккоректное значение')
            msg = bot.send_message(message.chat.id, 'Повторите попытку')
            bot.register_next_step_handler(msg, get_Age)
    else:
        bot.send_message(message.chat.id, 'Введенено неккоректное значение')
        msg = bot.send_message(message.chat.id, 'Повторите попытку')
        bot.register_next_step_handler(msg, get_Age)


def get_Gender(message):
    if message.text == 'Мужской':
        database.db_changeGender(message.from_user.id, 2)

        rmk = types.ReplyKeyboardMarkup()
        rmk.add(types.KeyboardButton('Мужчин'), types.KeyboardButton('Женщин'), types.KeyboardButton('Всех'))

        msg = bot.send_message(message.chat.id, 'Кого будем искать?', reply_markup=rmk)
        bot.register_next_step_handler(msg, get_MaleSearch)
    elif message.text == 'Женский':
        database.db_changeGender(message.from_user.id, 1)

        rmk = types.ReplyKeyboardMarkup()
        rmk.add(types.KeyboardButton('Мужчин'), types.KeyboardButton('Женщин'), types.KeyboardButton('Всех'))

        msg = bot.send_message(message.chat.id, 'Кого будем искать?', reply_markup=rmk)
        bot.register_next_step_handler(msg, get_MaleSearch)
    else:
        bot.send_message(message.chat.id, 'Введенено неккоректное значение')
        msg = bot.send_message(message.chat.id, 'Повторите попытку')
        bot.register_next_step_handler(msg, get_Gender)


def get_MaleSearch(message):
    if message.text == 'Мужчин':
        database.db_changeMaleSearch(message.from_user.id, 2)

        rmk = types.ReplyKeyboardRemove()

        msg = bot.send_message(message.chat.id, 'Укажите город!', reply_markup=rmk)
        bot.register_next_step_handler(msg, get_City)
    elif message.text == 'Женщин':
        database.db_changeMaleSearch(message.from_user.id, 1)

        rmk = types.ReplyKeyboardRemove()

        msg = bot.send_message(message.chat.id, 'Укажите город!', reply_markup=rmk)
        bot.register_next_step_handler(msg, get_City)
    elif message.text == 'Всех':
        database.db_changeMaleSearch(message.from_user.id, 3)

        rmk = types.ReplyKeyboardRemove()

        msg = bot.send_message(message.chat.id, 'Укажите город!', reply_markup=rmk)
        bot.register_next_step_handler(msg, get_City)
    else:
        bot.send_message(message.chat.id, 'Введенено неккоректное значение')
        msg = bot.send_message(message.chat.id, 'Повторите попытку')
        bot.register_next_step_handler(msg, get_MaleSearch)


def get_City(message):
    database.db_changeCity(message.from_user.id, message.text)

    msg = bot.send_message(message.chat.id, 'Расскажи что-то о себе. Это повысит шанс на взаимную симпатию:)')
    bot.register_next_step_handler(msg, get_userDescription)


def get_userDescription(message):
    database.db_changeDescription(message.from_user.id, message.text)

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
        final(message)
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
            database.db_prefer_val(message.from_user.id, message.text, message)
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
            database.insert_blob(message.user_from.id, src)
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
    bot.send_message(message.chat.id, 'Это ваша анкета')
    menu(message)


@bot.message_handler(commands='лайк')
def YouLiked(message):
    cursor.execute('SELECT Who FROM UserLike WHERE Whom=? AND Love=? ORDER BY ID DESC LIMIT 1', (message.from_user.id, False))
    database.Like(message.from_user.id, cursor.fetchall()[0])

    mem = message.from_user.username

    bot.send_message(message.chat.id, f'Приятного аппетита! \n Ваш чат: @{mem}')


@bot.message_handler(commands='дизлайк')
def YouDisLike(message):
    bot.send_message(message.chat.id, f'Не расстраивайся, скоро ты точно найдёшь свою половинку!')
    menu(message)


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
        item5 = types.KeyboardButton('👤 О себе')
        item6 = types.KeyboardButton('👤 Вкусы')
        item7 = types.KeyboardButton('👤 Фото')
        markup.add(item1, item2, item3, item4, item5, item6, item7)
        msg = bot.send_message(message.chat.id, 'Что хочешь изменить?', reply_markup=markup)
        bot.register_next_step_handler(msg, change_UserSettings)
    elif message.text == '🔍 Поиск':
        Search(message)
    else:
        bot.send_message(message.chat.id, 'Попробуем еще раз!')
        menu(message)


def change_Name(message):
    rmk = types.ReplyKeyboardRemove()

    if message.text == '👤 Имя':
        msg = bot.send_message(message.chat.id, 'Какое имя хотите взять на этот раз?', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_Name)
    else:
        database.db_changeName(message.from_user.id, message.text)
        bot.send_message(message.chat.id, 'Отлично, имя изменено')
        final(message)


def change_Age(message):
    rmk = types.ReplyKeyboardRemove()

    if message.text == '👤 Возраст':
        msg = bot.send_message(message.chat.id, 'Напишите ваш возраст по новой', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_Age)
    else:
        if int(message.text):
            if 100 >= int(message.text) > 0:
                database.db_changeAge(message.from_user.id, int(message.text))
                bot.send_message(message.chat.id, 'Отлично, возраст изменен')
                final(message)
            else:
                bot.send_message(message.chat.id, 'Введенено неккоректное значение')
                msg = bot.send_message(message.chat.id, 'Повторите попытку')
                bot.register_next_step_handler(msg, change_Age)
        else:
            bot.send_message(message.chat.id, 'Введенено неккоректное значение')
            msg = bot.send_message(message.chat.id, 'Повторите попытку')
            bot.register_next_step_handler(msg, change_Age)


def change_Gender(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Мужской'), types.KeyboardButton('Женский'))

    if message.text == '👤 Пол':
        msg = bot.send_message(message.chat.id, 'Укажи свой пол', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_Gender)
    else:
        if message.text == 'Мужской':
            database.db_changeGender(message.from_user.id, 2)
            bot.send_message(message.chat.id, 'Отлично, пол изменен, перейдем далее')
            change_MaleSearch('Смена')
        elif message.text == 'Женский':
            database.db_changeGender(message.from_user.id, 1)
            bot.send_message(message.chat.id, 'Отлично, пол изменен, перейдем далее')
            change_MaleSearch(message)
        else:
            bot.send_message(message.chat.id, 'Пол введен некорректно')
            msg = bot.send_message(message.chat.id, 'Повторите попытку')
            bot.register_next_step_handler(msg, change_Gender)


def change_MaleSearch(message):
    rmk = types.ReplyKeyboardMarkup()
    rmk.add(types.KeyboardButton('Мужчин'), types.KeyboardButton('Женщин'), types.KeyboardButton('Всех'))

    if message.text == 'Смена':
        msg = bot.send_message(message.chat.id, 'Кого будем искать?', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_MaleSearch)
    elif message.text == 'Мужчин':
        database.db_changeMaleSearch(message.from_user.id, 2)
        bot.send_message(message.chat.id, 'Отлично! Данные изменены')
        final(message)
    elif message.text == 'Женщин':
        database.db_changeMaleSearch(message.from_user.id, 1)
        bot.send_message(message.chat.id, 'Отлично! Данные изменены')
        final(message)
    elif message.text == 'Всех':
        database.db_changeMaleSearch(message.from_user.id, 3)
        bot.send_message(message.chat.id, 'Отлично! Данные изменены')
        final(message)
    else:
        bot.send_message(message.chat.id, 'Введено некорректное значение')
        msg = bot.send_message(message.chat.id, 'Повторите попытку')
        bot.register_next_step_handler(msg, change_MaleSearch)


def change_City(message):
    rmk = types.ReplyKeyboardRemove()

    if message.text == '👤 Город':
        msg = bot.send_message(message.chat.id, 'В каком городе вы живете теперь?', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_City)
    else:
        database.db_changeCity(message.from_user.id, message.text)
        bot.send_message(message.chat.id, 'Отлично, город изменен')
        final(message)


def change_Description(message):
    rmk = types.ReplyKeyboardRemove()

    if message.text == '👤 О себе':
        msg = bot.send_message(message.chat.id, 'Расскажите о себе', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_City)
    else:
        database.db_changeDescription(message.from_user.id, message.text)
        bot.send_message(message.chat.id, 'Отлично, описание изменено')
        final(message)


def change_Prefer_Menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('👤 Удалить предпочтение')
    item2 = types.KeyboardButton('👤 Добавить предпочтение')
    item3 = types.KeyboardButton('👤 Назад')
    markup.add(item1, item2, item3)

    if message.text == '👤 Вкусы':
        msg = bot.send_message(message.chat.id, 'Выбери действие', reply_markup=markup)
        bot.register_next_step_handler(msg, change_Prefer_Menu)
    elif message.text == '👤 Удалить предпочтение':
        change_Prefer_Delete(message)
    elif message.text == '👤 Добавить предпочтение':
        change_Prefer_Add(message)
    elif message.text == '👤 Назад':
        menu(message)
    else:
        bot.send_message(message.from_user.id, 'Введено некорректное значение')
        msg = bot.send_message(message.chat.id, 'Повторите попытку')
        bot.register_next_step_handler(msg, change_Prefer_Menu)


def change_Prefer_Delete(message):
    if message.text == '👤 Удалить предпочтение':
        rmk = types.ReplyKeyboardMarkup()
        rmk.add(types.KeyboardButton('Сохранить'))

        msg = bot.send_message(message.chat.id,
                               'Чтобы удалить предпочтение, напиши соответсвующие цифры в чат, как закончишь нажми на кнопку:\n\n'
                               '1 - Фастфуд\n'
                               '2 - Китайская кухня\n'
                               '3 - Японская кухня\n'
                               '4 - Грузинская кухня\n'
                               '5 - Итальянаская кухня\n', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_Prefer_Delete)

    elif message.text == 'Сохранить':
        bot.send_message(message.chat.id, 'Отлично, предпочтения изменены')
        menu(message)
    else:
        try:
            int(message.text)
        except ValueError:
            msg = bot.send_message(message.chat.id, 'Можно вводить только цифры!\nПопробуйте еще раз:')
            bot.register_next_step_handler(msg, change_Prefer_Delete)

        if int(message.text) > 5 or int(message.text) <= 0:
            msg = bot.send_message(message.chat.id,
                                   'Значение должно быть больше 0 и меньше или равно 5!\nПопробуйте еще раз:')
            bot.register_next_step_handler(msg, change_Prefer_Delete)
        else:
            database.db_deletePrefer(message.from_user.id, int(message), message)
            msg = bot.send_message(message.chat.id, 'Продолжайте!\nЕсли хотите закончить нажмите на кнопку:')
            bot.register_next_step_handler(msg, change_Prefer_Delete)


def change_Prefer_Add(message):
    if message.text == '👤 Добавить предпочтение':
        rmk = types.ReplyKeyboardMarkup()
        rmk.add(types.KeyboardButton('Сохранить'))

        msg = bot.send_message(message.chat.id,
                               'Чтобы добавить предпочтение, напиши соответсвующие цифры в чат, как закончишь нажми на кнопку:\n\n'
                               '1 - Фастфуд\n'
                               '2 - Китайская кухня\n'
                               '3 - Японская кухня\n'
                               '4 - Грузинская кухня\n'
                               '5 - Итальянаская кухня\n', reply_markup=rmk)
        bot.register_next_step_handler(msg, change_Prefer_Add)

    elif message.text == 'Сохранить':
        bot.send_message(message.chat.id, 'Отлично, предпочтения изменены')
        menu(message)
    else:
        try:
            int(message.text)
        except ValueError:
            msg = bot.send_message(message.chat.id, 'Можно вводить только цифры!\nПопробуйте еще раз:')
            bot.register_next_step_handler(msg, change_Prefer_Add)

        if int(message.text) > 5 or int(message.text) <= 0:
            msg = bot.send_message(message.chat.id,
                                   'Значение должно быть больше 0 и меньше или равно 5!\nПопробуйте еще раз:')
            bot.register_next_step_handler(msg, change_Prefer_Add)
        else:
            database.db_prefer_val(message.from_user.id, int(message), message)
            msg = bot.send_message(message.chat.id, 'Продолжайте!\nЕсли хотите закончить нажмите на кнопку:')
            bot.register_next_step_handler(msg, change_Prefer_Add)


def change_Photo(message):
    print(message)


def change_UserSettings(message):
    if message.text == '👤 Имя':
        change_Name(message)
    elif message.text == '👤 Возраст':
        change_Age(message)
    elif message.text == '👤 Пол':
        change_Gender(message)
    elif message.text == '👤 Город':
        change_City(message)
    elif message.text == '👤 О себе':
        change_Description(message)
    elif message.text == '👤 Вкусы':
        change_Prefer_Menu(message)
    elif message.text == '👤 Фото':
        get_firstPhoto(message)
    else:
        bot.send_message(message.chat.id, 'Попробуем еще раз!')
        menu_choice(message)


def Search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Лайк')
    item2 = types.KeyboardButton('Дизлайк')
    item3 = types.KeyboardButton('Меню')
    markup.add(item1, item2, item3)

    cursor.execute('SELECT * FROM User WHERE UserID=?', (message.from_user.id,))

    list1 = list()
    try:
        for i in database.search(message.from_user.id, cursor.fetchall()[5], cursor.fetchall()[4], cursor.fetchall()[3]):
            list1.append(i)
    except Exception:
        list1 = database.search(message.from_user.id, cursor.fetchall()[5], cursor.fetchall()[4], cursor.fetchall()[3])



    bot.send_message(message.chat.id, f"Имя: {list1[1]}\nВозраст: {list1[2]}\n Город: {list1[4]}\n О себе: \n {list1[6]}")

    if(message.text == 'Лайк'):
        cursor.execute('SELECT Count(*) FROM UserLike WHERE Who =? AND Love =? AND Whom=?', (message.from_user.id, False, list1[0]))
        if cursor.fetchall[0] > 0:
            bot.send_message(message.chat.id, f"Лайк оформлен")
            return




        database.Like(message.from_user.id, list1[0])
        bot.send_message(message.chat.id, f"Лайк оформлен")

        cursor.execute('SELECT ChatID FROM User WHERE UserID=?', list1[0])

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('/лайк')
        item2 = types.KeyboardButton('/дизлайк')

        markup.add(item1, item2)
        cursor.execute('SELECT * FROM User WHERE UserID=?', (message.from_user.id,))
        bot.send_message(cursor.fetchall()[0], f"Тебя кто-то лайкнул: \n Имя: {cursor.fetchall()[1]}\nВозраст: {cursor.fetchall()[2]}\n Город: {cursor.fetchall()[4]}\n О себе: \n {cursor.fetchall()[6]}", reply_markup = markup)

        Search(message)

        cursor.execute('SELECT Count(*) FROM UserLike WHERE Whom =? AND Love =? AND Who=?', (list1[0], False, message.from_user_id))

        if cursor.fetchall[0] > 0:  # Если есть те, кому ты нрав
            mem = message.from_user.username

            bot.send_message(message.chat.id, f'Взаимная симпатия! \n Ваш чат: @{mem}')

        return
    elif(message.text == 'Дизлайк'):
        bot.send_message(message.chat.id, f"Ищем дальше")
        Search(message)
    elif(message.text == 'Меню'):
        menu(message)


bot.infinity_polling()
