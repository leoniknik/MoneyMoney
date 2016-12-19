from mmhandler import MmHandler
import config
import telebot
import re

bot = telebot.TeleBot(config.token)
handler = MmHandler(0)  # по умолчанию user_id = 0
help_message = "добавить доход:\n+ {сумма} {название} {коммент}\nдобавить фиксированный доход:\n+ {сумма} {название} {дата} {коммент}\nдобавить расход:\n- {сумма} {категория} {коммент}\nпоказать категории:\nпокажи категории\nдобавить категорию:\nдобавь категорию {название}\nудалить категорию:\nудали категорию {название}\nпосмотреть отчет за месяц:\nотчет за {месяц}\nпосмотреть отчет за определенный период:\nотчет с {начальная дата} по {конечная дата}\nформат даты: xx-xx-xxxx"
report_periods = {'день', 'неделю', 'месяц', 'год'}

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
        length = len(str)
        if length == 0:
            bot.send_message(message.chat.id, 'Привет! Список моих команд:')
            bot.send_message(message.chat.id, help_message)
        elif str_array[0] == '+':
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
                
        elif str[0] == 'покажи' and str[1] == 'категории':
            handler_message = handler.show_categories()
            bot.send_message(message.chat.id, handler_message)
            
        elif len(str) == 3 and str[0] == 'добавь' and str[1] == 'категорию': #and re.match('[а-яa-z]+', str[2]):
            handler_message = handler.add_category(str[2])
            bot.send_message(message.chat.id, handler_message)
            
        elif str[0] == 'удали' and str[1] == 'категорию': #and re.match('[а-яa-z]+', str[2]):
            handler_message = handler.del_category(str[2])
            bot.send_message(message.chat.id, handler_message)
            
        elif len(str) >= 2 and str[0] == 'отчет':
            if str[1] == 'за' and (str[2] in report_periods):
                handler_message = handler.view_report(str[2])
                bot.send_message(message.chat.id, handler_message)
                # отчет за период
            elif str[1] == 'с' and re.match('\d{1,2}-\d{1,2}-\d{4}', str[2]) and str[3] == 'по' and \
                    re.match('\d{1,2}-\d{1,2}-\d{4}', str[4]):
                handler_message = handler.view_custom_report(str[2], str[4])
                bot.send_message(message.chat.id, handler_message)

        else:
            bot.send_message(message.chat.id, 'Привет! Список моих команд:')
            bot.send_message(message.chat.id, help_message)
            
    except Exception as e:
        handler_message = 'Ошибка: {} '.format(e)
        bot.send_message(message.chat.id, handler_message)
        
# бесконечная петля опроса
if __name__ == '__main__':
    bot.polling(none_stop=True)
