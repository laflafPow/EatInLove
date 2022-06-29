# в этом файле будут храниться все методы для взаимодействия с бд

import sqlite3
import base64
from pathlib import Path
from random import random

import telebot

# Подключаем бота

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

# Подключаем бд

conn = sqlite3.connect('db/UserDatabase.db', check_same_thread=False)
cursor = conn.cursor()


# Метод для внесения значений в таблицу User и сохранения изменений
def db_user_val(UserID: int, UserName: str, Age: int, GenderID: int, City: str, MaleSearchID: int, UserDescription: str,
                ChatID: int):
    cursor.execute(
        'INSERT INTO User (UserID, UserName, Age, GenderID, City, MaleSearchID, UserDescription, ChatID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
        (UserID, UserName, Age, GenderID, City, MaleSearchID, UserDescription, ChatID))
    conn.commit()


# Методы для изменения данных пользователя
def db_changeName(UserID: int, UserName: str):
    cursor.execute('UPDATE User SET UserName =? WHERE UserID = ?', (UserName, UserID))
    conn.commit()


def db_changeAge(UserID: int, Age: int):
    cursor.execute('UPDATE User SET Age =? WHERE UserID = ?', (Age, UserID))
    conn.commit()


def db_changeGender(UserID: int, GenderID: int):
    cursor.execute('UPDATE User SET GenderID =? WHERE UserID = ?', (GenderID, UserID))
    conn.commit()


def db_changeMaleSearch(UserID: int, MaleSearchID: int):
    cursor.execute('UPDATE User SET MaleSearchID =? WHERE UserID = ?', (MaleSearchID, UserID))
    conn.commit()


def db_changeCity(UserID: int, City: str):
    cursor.execute('UPDATE User SET City =? WHERE UserID = ?', (City, UserID))
    conn.commit()


def db_changeDescription(UserID: int, UserDescription: str):
    cursor.execute('UPDATE User SET UserDescription =? WHERE UserID = ?', (UserDescription, UserID))
    conn.commit()


def db_deletePrefer(UserID: int, FoodID: int, message):
    cursor.execute('SELECT Count() FROM UserFood WHERE UserID =? AND FoodID =?', (UserID, FoodID))

    if (cursor.fetchall()[0] == 0):
        bot.send_message(message.chat.id, 'Такого предпочтения нет!')
        return

    cursor.execute('DELETE FROM UserFood WHERE UserID = ? AND FoodID = ?', (UserID, FoodID))
    conn.commit()


# Метод внесения данных в таблицу Предпочтений(prefere)

def db_prefer_val(UserID, FoodID, message):
    cursor.execute('SELECT Count() FROM UserFood WHERE UserID =? AND FoodID =?', (UserID, FoodID))

    if (cursor.fetchall()[0] > 0):
        bot.send_message(message.chat.id, 'Вы уже добавили это предпочтение!')
        return

    cursor.execute('INSERT INTO UserFood (UserID, FoodID) VALUES (?, ?)',
                   (UserID, FoodID))
    conn.commit()


# -----------------------------------------------------------------------------

# Метод конвертирования картинки в бинарный вид


def img_bin(img, UserID):
    f = open(img, "rb")
    imgbin = f.read
    img_base = base64.encodestring(imgbin)
    cursor.execute('INSERT INTO UserPhoto (UserID, Photo) VALUES (?, ?)',
                   (UserID, img_base))
    conn.commit()


def save_photo(message):
    Path(f'files/{message.chat.id}/photos').mkdir(parents=True, exist_ok=True)

    # сохраним изображение
    file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = f'files/{message.chat.id}/' + file_info.file_path
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)
    return src


def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return encoded_string


def insert_blob(user_id, photo):
    try:
        sqlite_insert_blob_query = 'INSERT INTO UserPhoto (UserID, Photo) VALUES (?, ?)'
        user_photo = convert_to_binary_data(photo)

        # Преобразование данных в формат кортежа
        data_tuple = (user_id, user_photo)

        cursor.execute(sqlite_insert_blob_query, data_tuple)
        conn.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблиу")
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)


def img_dec(UserID):
    cursor.execute('SELECT Count() FROM UserPhoto WHERE UserID =?', (UserID))
    if (cursor.fetchall()[0] == 0):
        return
    else:
        cursor.execute('SELECT Photo FROM UserPhoto WHERE UserID =?', (UserID))
        img = base64.decodestring(cursor.fetchall()[0])


def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данный из blob сохранены в: ", filename, "\n")


# Метод добавления понравившихся пользователей
def Like(Who, Whom):
    cursor.execute('SELECT Count() FROM UserLike WHERE Whom =? AND Love =? AND Who=?', (Who, False, Whom))

    if cursor.fetchall[0] > 0:  # Если есть те, кому ты нрав
        cursor.execute('UPDATE UserLike SET Whom =? Love=? WHERE Who=?', (Who, True, Whom))
        conn.commit()


    elif cursor.fetchall[0] == 0:
        cursor.execute(
            'INSERT INTO UserLike (WhoLiked, WhomLiked) VALUES (?, ?)',
            (Who, Whom))
        conn.commit()


def search(UserID, MaleSearch, City, GenderID):
    cursor.execute('SELECT Count() From User Where UserID !=? and Gender=? and MaleSearch =?, City=?', UserID,
                   MaleSearch, GenderID, City)

    rndID = random.randint(1, cursor.fetchall()[0] + 1)
    while (rndID == UserID):
        rndID = random.randint(1, cursor.fetchall()[0] + 1)

    cursor.execute('SELECT * From User Where UserID =?', rndID)

    Search = list()
    bot.send_message(UserID, cursor.fetchall())
    for i in cursor.fetchall():
        bot.send_message(UserID, i)
        Search.append(i)

    return Search

##asdasdasd
