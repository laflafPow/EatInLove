# В этом файле будут храниться методы взаимодействия с пользователем

import telebot
token = '5270245996:AAEDYl1qVn02R-JFxF5HhrJ47RQwEItT3ww'
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start_message(message):
    sent_msg = bot.send_message(message.chat.id, 'Привет! Я помогу найти'
                                      ' тебе человека с которым '
                                      'ты сможешь хорошо провести время,'
                                      ' т.е. покушать, но для начала'
                                      ' расскажи чутка о себе,'
                                      ' чтобы я нашел подходящего человека...'
                                      '\n\nКак тебя зовут?')
    bot.register_next_step_handler(sent_msg, name_handler)