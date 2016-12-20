<<<<<<< HEAD
from mmhandler import MmHandler
import telebot
=======
import argparse
>>>>>>> 6a83fb8f81302a82db1b29ba55f65972225eec7a
import re
import logging

import yaml
import telebot

<<<<<<< HEAD
bot = telebot.TeleBot('280771706:AAG2jJxVekewCG_aTgcr2WQ3S6CcS7EZ_cg')
=======
from mmhandler import MmHandler

TOKEN = ''
bot = telebot.TeleBot(TOKEN)
>>>>>>> 6a83fb8f81302a82db1b29ba55f65972225eec7a
handler = MmHandler(0)  # по умолчанию user_id = 0
help_file = open('help.txt', 'r')
help_message = help_file.read()
help_file.close()
report_periods = {'день', 'неделю', 'месяц', 'год'}
category_mods = {'расходов', 'доходов'}
format_error = Exception('Неправильный формат команды!')


@bot.message_handler(commands=['start'])
def start(message):
    handler.user_id = message.chat.id
    handler_message = handler.start()
    bot.send_message(message.chat.id, handler_message)


@bot.message_handler(commands=['help'])
def help(message):
    handler.user_id = message.chat.id
    bot.send_message(message.chat.id, 'Привет! Список моих команд:')
    bot.send_message(message.chat.id, help_message)


@bot.message_handler(content_types=["text"])
def parse(message):
    handler.user_id = message.chat.id
    try:
        str_array = message.text.lower().split()
        length = len(str_array)

        # if empty line
        if length == 0:
            bot.send_message(message.chat.id, 'Забыл список команд? Держи:')
            bot.send_message(message.chat.id, help_message)
        elif length == 2 and (str_array[0] == "удалить" or str_array[0] == "удали") and str_array[1] == "другое":
            str_array[1]="other"
            handler_message = handler.del_category(str_array[1])
            bot.send_message(message.chat.id, handler_message)
        # if format +/-....
        elif str_array[0][0] == '+' or str_array[0][0] == '-':
            if length == 1:
                if re.match('[+]\d+', str_array[0]) or re.match('[-]\d+', str_array[0]):
                    handler_message = handler.add_operation(int(str_array[0]))
                    bot.send_message(message.chat.id, handler_message)
                else:
                    raise format_error

            elif length >= 2 and re.match('[а-яa-zА-ЯA-Z]+', str_array[1]):
                if re.match('[+]\d+', str_array[0]) or re.match('[-]\d+', str_array[0]):
                    if length >= 3:
                        description_buf = ' '.join(str_array[2:length])
                        handler_message = handler.add_operation(int(str_array[0]), str_array[1], description_buf)
                    else:
                        handler_message = handler.add_operation(int(str_array[0]), str_array[1])
                    bot.send_message(message.chat.id, handler_message)
                else:
                    raise format_error

        elif length >= 2 and (str_array[0] == 'показать' or str_array[0] == "покажи") and str_array[1] == 'категории':
            if length == 3:
                if str_array[2] in category_mods:
                    handler_message = handler.show_categories(str_array[2])
                    bot.send_message(message.chat.id, handler_message)
                else:
                    raise Exception('Неправильный формат команды!')
            else:
                handler_message = handler.show_categories()
                bot.send_message(message.chat.id, handler_message)

        elif length == 3 and str_array[1] == 'категорию' and re.match('[а-яa-zA-ZА-Я]+', str_array[2]):
            if str_array[0] == 'удалить' or str_array[0] == "удали":
                if str_array[2] == "другое":
                    bot.send_message(message.chat.id, "Для того чтобы удалить категорию другое и все операции связанные с ней, введите команду: удалить другое")
                    return
                handler_message = handler.del_category(str_array[2])
                bot.send_message(message.chat.id, handler_message)

            elif str_array[0] == 'добавить' or str_array[0] == 'добавь':
                handler_message = handler.add_category(str_array[2])
                bot.send_message(message.chat.id, handler_message)
            else:
                raise format_error

        elif str_array[0] == 'отчет':
            if length >= 3:
                if str_array[1] == 'за' and (str_array[2] in report_periods):
                    handler_message = handler.view_report(str_array[2])
                    bot.send_message(message.chat.id, handler_message)
                    bot.send_chat_action(message.chat.id, 'typing')
                    image_file = open('tmp/income.png', 'rb')
                    bot.send_photo(message.chat.id, image_file)
                    image_file = open('tmp/expense.png', 'rb')
                    bot.send_photo(message.chat.id, image_file)

                elif str_array[1] == 'с' and re.match('\d{1,2}-\d{1,2}-\d{4}', str_array[2]):
                    date_from_split_reverse = str_array[2].split('-')[::-1]
                    date_from = '-'.join(date_from_split_reverse)
                    if length >= 4 and str_array[3] == 'по' and re.match('\d{1,2}-\d{1,2}-\d{4}', str_array[4]):
                        date_to_split_reverse = str_array[4].split('-')[::-1]
                        date_to = '-'.join(date_to_split_reverse)
                        handler_message = handler.view_custom_report(date_from, date_to)
                    else:
                        handler_message = handler.view_custom_report(date_from)
                    bot.send_message(message.chat.id, handler_message)
                    bot.send_chat_action(message.chat.id, 'typing')
                    image_file = open('tmp/income.png', 'rb')
                    bot.send_photo(message.chat.id, image_file)
                    image_file = open('tmp/expense.png', 'rb')
                    bot.send_photo(message.chat.id, image_file)
                else:
                    raise format_error

            elif length == 1:
                keyboard = telebot.types.InlineKeyboardMarkup()
                button_month = telebot.types.InlineKeyboardButton(text="месяц", callback_data="месяц")
                button_day = telebot.types.InlineKeyboardButton(text="день", callback_data="день")
                button_week = telebot.types.InlineKeyboardButton(text="неделя", callback_data="неделю")
                button_year = telebot.types.InlineKeyboardButton(text="год", callback_data="год")
                keyboard.add(button_day)
                keyboard.add(button_week)
                keyboard.add(button_month)
                keyboard.add(button_year)
                bot.send_message(message.chat.id, "Выбери период", reply_markup=keyboard)
            else:
                raise format_error

        else:
            bot.send_message(message.chat.id, 'Не знаю такой команды! Список моих команд:')
            bot.send_message(message.chat.id, help_message)

    except Exception as e:
        handler_message = 'Ошибка: {} '.format(e)
        bot.send_message(message.chat.id, handler_message)


# handler for inline-keyboard
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data in report_periods:
            handler_message = handler.view_report(call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=handler_message)
            bot.send_chat_action(call.message.chat.id, 'typing')
            image_file = open('tmp/income.png', 'rb')
            bot.send_photo(call.message.chat.id, image_file)
            image_file = open('tmp/expense.png', 'rb')
            bot.send_photo(call.message.chat.id, image_file)


# бесконечная петля опроса
if __name__ == '__main__':
    token = ""
    parser = argparse.ArgumentParser(description='Process some flags.')
    # parser.add_argument('-o', '--output')
    # parser.add_argument('-v', dest='verbose', action='store_true')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--develop', help='Develop dirs', action="store_true")
    group.add_argument('--production', help='Production dirs', action="store_true")
    args = parser.parse_args()

    if args.develop:
        yaml_config = open('../config/config.yaml', 'r')
    elif args.prod:
        yaml_config = open('/etc/moneymoney.d/config.yaml', 'r')
    else:
        ArgumentParser.error("You should specify either --develop or --production option!")

    config = yaml.load(yaml_config)
    print(config)
    TOKEN = config['token']

    print(TOKEN)

    logger = telebot.logger
    telebot.logger.setLevel(logging.DEBUG)

    bot.token = TOKEN
    bot.polling(none_stop=True)
