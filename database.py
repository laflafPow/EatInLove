# в этом файле будут храниться все методы для взаимодействия с бд

import sqlite3
import base64
from pathlib import Path

import telebot

# Подключаем бота

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

# Подключаем бд

conn = sqlite3.connect('db/UserDatabase.db', check_same_thread=False)
cursor = conn.cursor()


# Метод для внесения значений в таблицу User и сохранения изменений

def db_user_val(UserID: int, UserName: str, Age: int, GenderID: int, City: str, MaleSearchID: int, UserDescription: str):
    cursor.execute(
        'INSERT INTO User (UserID, UserName, Age, GenderID, City, MaleSearchID, UserDescription) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (UserID, UserName, Age, GenderID, City, MaleSearchID, UserDescription))
    conn.commit()


# Метод внесения данных в таблицу Предпочтений(prefere)

def db_prefer_val(UserID, FoodID, message):
    cursor.execute('SELECT Count() FROM UserFood WHERE UserID =? AND FoodID =?', (UserID, FoodID))

    if (cursor.fetchone()[0] > 0):
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
    if(cursor.fetchone()[0] == 0):
        return
    else:
        cursor.execute('SELECT Photo FROM UserPhoto WHERE UserID =?', (UserID))
        img = base64.decodestring(cursor.fetchone()[0])

def write_to_file(data, filename):
    # Преобразование двоичных данных в нужный формат
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данный из blob сохранены в: ", filename, "\n")

# Метод добавления понравившихся пользователей
def Like(Who, Whom):
    cursor.execute(
        'INSERT INTO UserLike (WhoLiked, WhomLiked) VALUES (?, ?)',
        (Who, Whom))
    conn.commit()

##asdasdasd
