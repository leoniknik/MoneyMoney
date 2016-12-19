from mmhandler import MmHandler
import config
import telebot
import re

bot = telebot.TeleBot(config.token)
handler = MmHandler(0)  # по умолчанию user_id = 0
help_message = "добавить доход:\n+{сумма} {категория} {комментарий}\nдобавить расход:\n-{сумма} {категория} {комментарий}\nпоказать категории:\nпокажи категории {расходов} {доходов}\nдобавить категорию:\nдобавь категорию {название}\nудалить категорию:\nудали категорию {название}\nпосмотреть отчет за месяц:\nотчет за {месяц}\nпосмотреть отчет за определенный период:\nотчет с {начальная дата} по {конечная дата}\nформат даты: xx-xx-xxxx"
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
        
        # if format +/-....
        elif str_array[0][0] == '+'  or str_array[0][0] == '-':
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
                       
        elif length >= 2 and str_array[0] == 'покажи' and str_array[1] == 'категории':
            if length == 3:
                if str_array[2] in category_mods:
                    handler_message = handler.show_categories(str_array[2])
                else:
                    raise Exception('Неправильный формат команды!')
            else:
                handler_message = handler.show_categories()
                bot.send_message(message.chat.id, handler_message)
            
        elif length == 3 and and str_array[1] == 'категорию' and re.match('[а-яa-zA-ZА-Я]+', str_array[2]):
            if str_array[0] == 'удали':
                handler_message = handler.del_category(str_array[2])
                bot.send_message(message.chat.id, handler_message)
                
            elif str_array[0] == 'добавь':
                handler_message = handler.add_category(str_array[2])
                bot.send_message(message.chat.id, handler_message)
            else:
                raise format_error
            
        elif length >= 3 and str_array[0] == 'отчет' and :
            if str_array[1] == 'за' and (str_array[2] in report_periods):
                handler_message = handler.view_report(str_array[2])
                bot.send_message(message.chat.id, handler_message)
                
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
            else:
                raise format_error

        else:
            bot.send_message(message.chat.id, 'Не знаю такой команды! Список моих команд:')
            bot.send_message(message.chat.id, help_message)
            
    except Exception as e:
        handler_message = 'Ошибка: {} '.format(e)
        bot.send_message(message.chat.id, handler_message)
        
# бесконечная петля опроса
if __name__ == '__main__':
    bot.polling(none_stop=True)
