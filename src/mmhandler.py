from sql_module.sql import SQL
import datetime
from dateutil import relativedelta
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
from matplotlib import rc

font = {'family': 'Verdana',
        'weight': 'normal'}
rc('font', **font)


"""
MoneyMoney handler for all calculating functions.
"""


# # маленький контекстный менеджер для работы с БД
# class Sqltor(object):
#     def __init__(self, sql):
#         self.sql = sql
#         self.sql.open()
#
#     def __enter__(self):
#         return self.sql
#
#     def __exit__(self, *args):
#         self.sql.close()

# function for graph design
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.1f}%\n ({v:d})'.format(p=pct, v=val)

    return my_autopct


class MmHandler:
    def __init__(self, user_id):
        self.user_id = user_id
        try:
            self.sql = SQL()
        except Exception as e:
            print('Ошибка при создании базы данных: {}'.format(e))

    def start(self):
        try:
            self.sql.add_user(self.user_id)
        except Exception as e:
            return 'Ошибка при инициализации: {} '.format(e)
        else:
            return 'Привет! Чтобы узнать о моих возможностях,' \
                   'воспользуйся командой /help'

    def add_operation(self, amount, category=None, description=None, date=None):
        try:
            if category is None:
                category = 'other'
            categories = set(self.sql.get_all_categories(self.user_id))
            if category in categories:
                self.sql.add_operation(self.user_id, amount, category, date, description)
            else:
                if category == "other":
                    self.add_category(category)
                    self.sql.add_operation(self.user_id, amount, category, date, description)
                    return 'Операция успешно добавлена.'
                else:
                    return 'Такой категории не существует! Воспользуйтесь ' \
                       'функцией "добавить категорию".'
        except Exception as e:
            return 'Операция не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Операция успешно добавлена.'

    def show_categories(self, mode=None):
        try:
            if mode == 'доходов':
                categories_list = self.sql.get_income_categories(self.user_id)
            elif mode == 'расходов':
                categories_list = self.sql.get_expense_categories(self.user_id)
            else:
                categories_list = self.sql.get_all_categories(self.user_id)
        except Exception as e:
            return 'Вывод категорий невозможен! Ошибка: {} '.format(e)
        else:
            if categories_list.count("other") != 0:
                categories_list.remove("other")
                categories_list.append("другое")
            message = 'Список категорий: ' + ', '.join(categories_list)
            return message

    def add_category(self, name):
        try:
            self.sql.add_category(name, self.user_id)
        except Exception as e:
            return 'Категория не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно добавлена.'

    def del_category(self, name):
        try:
            ### оберег
            if name=="other":
                self.sql.delete_category_other(self.user_id)
            ### конец оберега
            else:
                self.sql.delete_category(name, self.user_id)
        except Exception as e:
            return 'Категория не была удалена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно удалена.'

    def view_report(self, period=None):
        if period == 'год':
            delta = relativedelta.relativedelta(years=1)
        elif period == 'месяц':
            delta = relativedelta.relativedelta(months=1)
        elif period == 'неделю':
            delta = relativedelta.relativedelta(weeks=1)
        elif period == 'день':
            delta = relativedelta.relativedelta(days=1)
        else:
            delta = None
        try:
            if delta is None:
                history = self.sql.get_history(self.user_id)
            else:
                date_to = datetime.datetime.now()
                date_from_str = (date_to - delta).strftime("%Y-%m-%d")
                date_to_str = date_to.strftime("%Y-%m-%d")
                history = self.sql.get_history(self.user_id, date_from_str, date_to_str)
        except Exception as e:
            return 'Получить историю невозможно! Ошибка: {} '.format(e)
        else:
            # graph design
            plt.rcParams['font.size'] = 24.0
            # for windows!
            #font = {'family': 'Verdana'}
            #rc('font', **font)
            labels_income = []
            labels_expense = []
            values_income = []
            values_expense = []
            dict_income = {}
            dict_expense = {}
            for item in history:
                    if item[0] >= 0:
                        if dict_income.get(item[1]) is None:
                            dict_income[item[1]] = item[0]
                        else:
                            dict_income[item[1]] = dict_income[item[1]] + item[0]
                    else:
                        if dict_expense.get(item[1]) is None:
                            dict_expense[item[1]] = item[0]
                        else:
                            dict_expense[item[1]] = dict_expense[item[1]] + item[0]
            legend_in = []
            legend_ex = []
            in_i = 0
            ex_i = 0
            for key, val in dict_income.items():
                    if key == "other":
                        labels_income.append(str(in_i))
                        legend_in.append(str(in_i)+' : '+ str(key))
                        in_i += 1
                    else:
                        labels_income.append(str(in_i))
                        legend_in.append(str(in_i) + ' : ' + str(key))
                        in_i += 1
                    values_income.append(val)

            for key, val in dict_expense.items():
                    if key == "other":
                        labels_expense.append(str(ex_i))
                        legend_ex.append(str(ex_i) + ' : ' + str(key))
                        ex_i += 1
                    else:
                        labels_expense.append(str(ex_i))
                        legend_ex.append(str(ex_i) + ' : ' + str(key))
                        ex_i += 1
                    values_expense.append(abs(val))

            # color scheme
            color_map = cm.get_cmap('Pastel1')
            num_of_colors_income = len(values_income)
            num_of_colors_expense = len(values_expense)

            colors_income = color_map([x / float(num_of_colors_income) for x in range(num_of_colors_income)])
            colors_expense = color_map([x / float(num_of_colors_expense) for x in range(num_of_colors_expense)])

            #income
            fig_income = plt.figure()
            plt.pie(values_income, labels=labels_income, colors=colors_income, autopct=make_autopct(values_income), startangle=140)
            plt.axis('equal')


            if not os.path.exists('tmp'):
                os.makedirs('tmp')
            fig_income.savefig('tmp/income'+str(self.user_id)+'.png')
            plt.close()
            fig_expense = plt.figure()
            plt.pie(values_expense, labels=labels_expense, colors=colors_expense, autopct=make_autopct(values_expense),
                    startangle=140)
            plt.axis('equal')


            if not os.path.exists('tmp'):
                os.makedirs('tmp')
            fig_expense.savefig('tmp/expense'+str(self.user_id)+'.png')
            plt.close()
            message = 'История операций за'
            if period is not None:
                message += ' {}'.format(period)
            str_history = ""
            for item in history:
                str_history += str(item[1]) + ": " + str(item[0]) + " комментарий: " + item[3] + '\n'
            #str_history = str(history)[1:-1]
            return message + '\n' + str_history + '\n' + str(legend_in) + '\n' + str(legend_ex)

    def view_custom_report(self, date_from, date_to=None):

        try:
            if date_to is None:
                history = self.sql.get_history(self.user_id, date_from)
            else:
                history = self.sql.get_history(self.user_id, date_from, date_to)
        except Exception as e:
            return 'Получить историю невозможно! Ошибка: {} '.format(e)
        else:
            message = 'История операций c {}'.format(date_from)
            if date_to is not None:
                message += ' по {}'.format(date_to)
            str_history = ""
            for item in history:
                str_history += str(item[1]) + ": " + str(item[0]) + " комментарий: " + item[3] + '\n'
            return message + '\n' + str_history
