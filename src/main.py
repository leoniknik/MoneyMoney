from mmhandler import MmHandler
# from sql import SQL
import config
import telebot
import re

"""
TODO:
Оповещения (Ты забыл обо мне?)
Разобрать выражение на естественном языке
"""

bot = telebot.TeleBot(config.token)
handler = MmHandler(0)  # по умолчанию user_id = 0


# прикрутить вебхуки
# прикрутить разбор сообщения на естественном языке


# для тестирования
@bot.message_handler(commands=['start'])
def start(message):
    handler.user_id = message.chat.id
    handler_message = handler.start()
    bot.send_message(message.chat.id, handler_message)


@bot.message_handler(commands=['help'])
def help(message):
    handler.user_id = message.chat.id
    help_str = "добавить доход:\n+ {сумма} {название} {коммент}\nдобавить фиксированный доход:\n+ {сумма} {название} {дата} {коммент}\nдобавить расход:\n- {сумма} {категория} {коммент}\nпоказать категории:\nпокажи категории\nдобавить категорию:\nдобавь категорию {название}\nудалить категорию:\nудали категорию {название}\nпосмотреть отчет за месяц:\nотчет за {месяц}\nпосмотреть отчет за определенный период:\nотчет с {начальная дата} по {конечная дата}\nформат даты: xx.xx.xxxx"
    bot.send_message(message.chat.id, 'Hello. This you can do:')
    bot.send_message(message.chat.id, help_str)


@bot.message_handler(content_types=["text"])
def parse(message):


    try:
        handler.user_id = message.chat.id
        str = message.text.lower().split()
        length = len(str)
        if length == 0:
            pass  # вставить вызов help
        elif str[0] == '+':
            if length == 3:
                if re.match('\d+', str[1]) and re.match('[а-яa-z]+', str[2]):
                    handler_message = handler.add_operation(int(str[0] + str[1]), str[2])
                    bot.send_message(message.chat.id, handler_message)
                    # вызов доход amount category
            elif length >= 4:
                if length >= 4 and re.match('\d+', str[1]) and re.match('[а-яa-z]+', str[2]):
                    buf = ' '.join(str[3:length])
                    handler_message = handler.add_operation(int(str[0] + str[1]), str[2], buf)
                    bot.send_message(message.chat.id, handler_message)
                    # вызов доход amount category description
        elif str[0] == '-':
            if length == 3 and re.match('\d+', str[1]) and re.match('[а-яa-z]+', str[2]):
                handler_message = handler.add_operation(int(str[0] + str[1]), str[2])
                bot.send_message(message.chat.id, handler_message)
                # расход amount category
            elif length > 3 and re.match('\d+', str[1]) and re.match('[а-яa-z]+', str[2]):
                buf = ' '.join(str[3:length])
                handler_message = handler.add_operation(int(str[0] + str[1]), str[2], buf)
                bot.send_message(message.chat.id, handler_message)
                # расход amount category description
        elif str[0] == 'покажи':
            if str[1] == 'категории':
                handler_message = handler.show_categories()
                bot.send_message(message.chat.id, handler_message)
                # h = категории
        elif len(str) == 3 and str[0] == 'добавь' and str[1] == 'категорию' and re.match('[а-яa-z]+', str[2]):
            handler_message = handler.add_category(str[2])
            bot.send_message(message.chat.id, handler_message)
            # добавь категорию
        elif str[0] == 'удали' and str[1] == 'категорию' and re.match('[а-яa-z]+', str[2]):
            handler_message = handler.del_category(str[2])
            bot.send_message(message.chat.id, handler_message)
            # удали категорию
        elif len(str) >= 2 and str[0] == 'отчет':
            if str[1] == 'за' and re.match('[а-яa-z]+', str[2]):
                handler_message = handler.view_report(str[2])
                bot.send_message(message.chat.id, handler_message)
                # отчет за период
            if str[1] == 'с' and re.match('\d{1,2}-\d{1,2}-\d{4}', str[2]) and str[3] == 'по' and \
                    re.match('\d{1,2}-\d{1,2}-\d{4}', str[4]):
                handler_message = handler.view_custom_report(str[2], str[4])
                bot.send_message(message.chat.id, handler_message)
                # отчет с date по date
        else:
            pass  # вызов help
    except Exception as e:
        print(e)
  # бесконечная петля опроса
if __name__ == '__main__':
    bot.polling(none_stop=True)
