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
    cursor.execute('INSERT INTO test (UserName, Age, GenderID, CityID, MaleSearch, Discription) VALUES (?, ?, ?, ?, ?, ?)',
                   (UserName, Age, GenderID, CityID, MaleSearch, Discription))
    conn.commit()



#Метод внесения данных в таблицу Предпочтений(prefere)

def db_prefer_val(UserID, FoodID):
    cursor.execute('SELECT UserID From User Where UserName =?', UserName) #Конвертируем UserName в UserID
    UserID = cursor.fetchone()
    UserID = UserID[1]

    cursor.execute('SELECT FoodID From User Where FoodName =?', FoodName)
    FoodID = cursor.fetchone()
    FoodID = FoodID[1]

    cursor.execute('INSERT INTO prefere (UserID, FoodID) VALUES (?, ?)',
                   (UserID, FoodID))
    conn.commit()
#-----------------------------------------------------------------------------

#Метод конвертирования картинки в бинарный вид
def img_bin(img_path):
    f = open(img_path, "rb")
    imgbin = f.read
    return imgbin

