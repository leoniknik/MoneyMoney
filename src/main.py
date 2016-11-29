from mmhandler import MmHandler
#from sql import SQL

import argparse
import re
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


if __name__ == '__main__':
    token = ""
    parser = argparse.ArgumentParser(description='Process some flags.')
    # parser.add_argument('-o', '--output')
    # parser.add_argument('-v', dest='verbose', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--develop', help='Develop dirs', action="store_true")
    group.add_argument('--prod', help='Production dirs', action="store_true")
    args = parser.parse_args()

    if args.develop:
        with open('../config/config', 'r') as f:
            token = re.sub("[\'\n]+", "", f.readline().split(' = ')[1])
    elif args.prod:
        with open('/etc/moneymoney.d/config', 'r') as f:
            token = re.sub("\'\n", "", f.readline().split(' = ')[1])

    print(token)
    bot = telebot.TeleBot(token)
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

    # The Big polling Loop
    bot.polling(none_stop = True)
