from mmhandler import MmHandler
#from sql import SQL
import config
import telebot
"""
TODO:
Оповещения (Ты забыл обо мне?)
Разобрать выражение на естественном языке
11) start
12) help
13) main
14) формирование ответного сообщения
прикрутить передачу trace ошибок из SQL
"""

bot = telebot.TeleBot(config.token)
handler = MmHandler(0) # по умолчанию user_id = 0
# прикрутить вебхуки
# прикрутить разбор сообщения на естественном языке

# для тестирования
@bot.message_handler(commands=['start'])
def start(message):
    MmHandler.user_id = message.chat.id
    if (MmHandler.start):
        bot.send_message(message.chat.id, 'Hello. Let\'s start from help command')
    else:
        bot.send_message(message.chat.id, 'Undefined error')

@bot.message_handler(commands=['help'])
def help(message):
    pass

# бесконечная петля опроса
if __name__ == '__main__':
    bot.polling(none_stop=True)
