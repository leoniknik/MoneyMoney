from sql_module.sql import SQL
import datetime
from dateutil import relativedelta

"""
MoneyMoney handler for all calculating functions.
List of functions:
(+) - completed
(?) - WTF function
(+) start(user_id)
    RETURN {int_code, str_message)
    str_message to user
    code: 0 - unsuccessful
    code: 1 - successful
(?) add_fixed_income(name, amount, date)
(?) del_fixed_income(name, date)
(+) add_operation(amount, category, description, date)
    RETURN str_message
(+) show_categories(mode) mode may be income, expense, None
    RETURN str_message
(?) show_incomes()
(+) add_category(name)
    RETURN str_message
(+) del_category(name)
    RETURN str_message
(+) view_report(period, category = None) period may be year, months, week, day
    RETURN str_message
(+) view_custom_report(date_from, date_to = None, category = None)
    RETURN str_message

"""


# маленький контекстный менеджер для работы с БД
class Sqltor(object):
    def __init__(self, sql):
        self.sql = sql
        self.sql.open()

    def __enter__(self):
        return self.sql

    def __exit__(self, *args):
        self.sql.close()


class MmHandler:
    def __init__(self, user_id):
        self.user_id = user_id
        try:
            self.sql = SQL()
        except Exception as e:
            print('Ошибка при создании базы данных: {}'.format(e))

    def start(self):
        try:
            with Sqltor(self.sql) as db:
                db.add_user(self.user_id)
        except Exception as e:
            return 0, 'Ошибка при инициализации: {} '.format(e)
        else:
            return (1, 'Привет! Чтобы узнать о моих возможностях,'
                       'воспользуйся командой /help')

    def add_fixed_income(self, name, amount, date):
        return 'Я пустышка и моя жизнь - тлен'

    def del_fixed_income(self, name, date):
        return 'Я пустышка и моя жизнь - тлен'

    def add_operation(self, amount, category=None, description=None, date=None):
        try:
            with Sqltor(self.sql) as db:
                categories = set(db.get_all_categories(self.user_id))
                if category in categories:
                    db.add_operation(self.user_id, amount, category, description, date)
                else:
                    return 'Такой категории не существует! Воспользуйтесь ' \
                           'функцией "добавить категорию".'
        except Exception as e:
            return 'Операция не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Операция успешно добавлена.'

    def show_categories(self, mode=None):
        try:
            with Sqltor(self.sql) as db:
                if mode == 'income':
                    categories_list = db.get_income_categories(self, self.user_id)
                elif mode == 'expense':
                    categories_list = db.get_expense_categories(self, self.user_id)
                else:
                    categories_list = db.get_all_categories(self, self.user_id)
        except Exception as e:
            return 'Вывод категорий невозможен! Ошибка: {} '.format(e)
        else:
            message = 'Список категорий:' + ', '.join(categories_list)
            return message

    def add_category(self, name):
        try:
            with Sqltor(self.sql) as db:
                db.add_category(name, self.user_id)
        except Exception as e:
            return 'Категория не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно добавлена.'

    def del_category(self, name):
        try:
            with Sqltor(self.sql) as db:
                db.delete_category(name, self.user_id)
        except Exception as e:
            return 'Категория не была удалена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно удалена.'

    # в перспективе слить отчеты в одну функцию
    def view_report(self, period=None, category=None):
        if period == 'year':
            delta = relativedelta.relativedelta(years=1)
        elif period == 'month':
            delta = relativedelta.relativedelta(months=1)
        elif period == 'week':
            delta = relativedelta.relativedelta(weeks=1)
        elif period == 'day':
            delta = relativedelta.relativedelta(days=1)
        else:
            delta = None
        try:
            with Sqltor(self.sql) as db:
                if delta is None:
                    history = db.get_history(self.user_id)
                else:
                    date_to = datetime.datetime.now()
                    date_from_str = (date_to - delta).strftime("%Y-%m-%d")
                    date_to_str = date_to.strftime("%Y-%m-%d")
                    history = db.get_history(self.user_id, date_from_str, date_to_str)
        except Exception as e:
            return 'Получить историю невозможно! Ошибка: {} '.format(e)
        else:
            message = 'История операций'
            if period is not None:
                message += ' {}'.format(period)
            return message + '\n' + history

    def view_custom_report(self, date_from, date_to=None, category=None):
        try:
            with Sqltor(self.sql) as db:
                history = db.get_history(self.user_id, date_from, date_to)
        except Exception as e:
            return 'Получить историю невозможно! Ошибка: {} '.format(e)
        else:
            message = 'История операций c {}'.format(date_from)
            if date_to is not None:
                message += ' по {}'.format(date_to)
            return message + '\n' + history
