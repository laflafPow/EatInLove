# в этом файле будут храниться все методы для взаимодействия с бд

import sqlite3
import telebot

# Подключаем бота

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

# Подключаем бд

conn = sqlite3.connect('db/UserDatabase.db', check_same_thread=False)
cursor = conn.cursor()

# Метод для внесения значений в таблицу User и сохранения изменений

def db_user_val(UserName: str, Age: int, GenderID: int, CityID: int):
    cursor.execute('INSERT INTO test (UserName, Age, GenderID, CityID) VALUES (?, ?, ?, ?)',
                   (UserName, Age, GenderID, CityID))
    conn.commit()