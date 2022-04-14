# Основной файл, где будет проходить главный поток программы

import telebot
import database
import userInteraction

# в файле database будут храниться все методы для взаимодействия с бд

token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

userInteraction.start_message()

userlist = []


def name_handler(pm):
    name = pm.text
    userlist.insert(name)
    sent_msg = bot.send_message(pm.chat.id, f"Ладно, {name}, а сколько тебе лет?")
    bot.register_next_step_handler(sent_msg, age_handler, name)


def age_handler (pm, name):
    age = pm.text
    userlist.insert(age)
    sent_msg = (pm.chat.id, f"Приятно познакомиться, перейдем на следующий этап. Из какого ты города?")
    bot.register_next_step_handler(sent_msg, city_handler)


def city_handler(pm):
    city = pm.text
    info = cursor.execute(f"SELECT * FROM City WHERE [Name]={city}")
    if info.fetchone() is None:
        bot.send_message('Этот город мы еще не поддерживаем :c У нас есть только Москва и Санкт-Петербург')
    else:
        print(info)

bot.polling(none_stop=True)
