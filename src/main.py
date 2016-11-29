from mmhandler import MmHandler
# from sql import SQL
import config
import telebot
import re

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
handler = MmHandler(0)  # по умолчанию user_id = 0


# прикрутить вебхуки
# прикрутить разбор сообщения на естественном языке


# для тестирования
@bot.message_handler(commands=['start'])
def start(message):
    MmHandler.user_id = message.chat.id
    if MmHandler.start:
        bot.send_message(message.chat.id, 'Hello. Let\'s start from help command')
    else:
        bot.send_message(message.chat.id, 'Undefined error')


@bot.message_handler(commands=['help'])
def help(message):
    help_str = "добавить доход:\n+ {сумма} {название} {коммент}\nдобавить фиксированный доход:\n+ {сумма} {название} {дата} {коммент}\nдобавить расход:\n- {сумма} {категория} {коммент}\nпоказать категории:\nпокажи категории\nдобавить категорию:\nдобавь категорию {название}\nудалить категорию:\nудали категорию {название}\nпосмотреть отчет за месяц:\nотчет за {месяц}\nпосмотреть отчет за определенный период:\nотчет с {начальная дата} по {конечная дата}\nформат даты: xx.xx.xxxx"
    bot.send_message(message.chat.id, 'Hello. This you can do:')
    bot.send_message(message.chat.id, help_str)


@bot.message_handler(content_types=["text"])
def parse(message):
    handler.user_id = message.chat.id
    str = message.text.split()
    length = len(str)
    if length == 0:
        pass  # вставить вызов help
    elif str[0] == '+':
        if length == 3:
            if re.match('\d+', str[1]) and re.match('[а-яА-я]+', str[2]):
                handler.add_operation(str[1], str[2])
                # вызов доход amount category
        elif length >= 4:
            if length >= 4 and re.match('\d+', str[1]) and re.match('[а-яА-я]+', str[2]):
                buf = ' '.join(str[3:length])
                handler.add_operation(str[1], str[2], buf)
                # вызов доход amount category description
    elif str[0] == '-':
        if length == 3 and re.match('\d+', str[1]) and re.match('[а-яА-я]+', str[2]):
            handler.add_operation(str[1], str[2])
            # расход amount category
        elif length > 3 and re.match('\d+', str[1]) and re.match('[а-яА-я]+', str[2]):
            buf = ' '.join(str[3:length])
            handler.add_operation(str[1], str[2], buf)
            # расход amount category description
    elif str[0] == 'покажи':
        if str[1] == 'категории':
            handler.show_categories()
            # категории
    elif str[0] == 'добавь' and str[1] == 'категорию' and re.match('[а-яА-я]+', str[2]):
        handler.add_category(str[2])
        # добавь категорию
    elif str[0] == 'удали' and str[1] == 'категорию' and re.match('[а-яА-я]+', str[2]):
        handler.del_category(str[2])
        # удали категорию
    elif str[0] == 'отчет':
        if str[1] == 'за' and re.match('[а-яА-я]+', str[2]):
            handler.view_report(str[2])
            # отчет за период
        if str[1] == 'с' and re.match('\d{1,2}.\d{1,2}.\d{4}', str[2]) and str[3] == 'по' and \
                re.match('\d{1,2}.\d{1,2}.\d{4}', str[4]):
            handler.view_custom_report(str[2], str[4])
            # отчет с date по date
    else:
        pass  # вызов help


# бесконечная петля опроса
if __name__ == '__main__':
    bot.polling(none_stop=True)
