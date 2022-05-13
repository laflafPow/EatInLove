# в этом файле будут храниться все методы для взаимодействия с бд

import sqlite3
import telebot
import random


# Подключаем бота

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

# Подключаем бд

conn = sqlite3.connect('db/UserDatabase.db', check_same_thread=False)
cursor = conn.cursor()

# Метод для внесения значений в таблицу User и сохранения изменений

def db_user_val(UserName: str, Age: int, GenderID: int, CityID: int):
    cursor.execute('INSERT INTO User (UserName, Age, GenderID, CityID, MaleSearch, Discription) VALUES (?, ?, ?, ?, ?, ?)',
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
def img_bin(img):
    f = open(img, "rb")
    imgbin = f.read
    return imgbin

#Метод добавления понравившихся пользователей
def Like(Who, Whom):

    cursor.execute(
        'INSERT INTO UserLike (WhoLiked, WhomLiked) VALUES (?, ?)',
        (Who, Whom))
    conn.commit()

##asdasdasd




def search(UserID, MaleSearch):
    cursor.execute('SELECT Count(*) From User')
    rndID = random.randint(1, cursor.fetchone()[0] + 1)
    while(rndID == UserID):
        rndID = random.randint(1, cursor.fetchone()[0]+1)

    cursor.execute('SELECT MaleSearch From User Where UserID !=? and Gender=? and MaleSearch =?', rndID, MaleSearch, GenderID)


    #Данные предложенного человека из поиска:
    SuserID
    SuserName
    SuserAge
    SuserGenderID


