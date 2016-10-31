from sql import SQL

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
(+)add_operation(amount, category, description, date)
    RETURN str_message
show_income_categories()
show_incomes()
show_daily_operations(category = None)
(+) add_category(name)
    RETURN str_message
(+) del_category(name)
    RETURN str_message
view_report(period, category = None)
view_custom_report(start_date, end_date = None, category = None)

"""


class MmHandler:
    def __init__(self, user_id):
        self.user_id = user_id
        try:
            self.sql = SQL()
        except Exception as e:
            print('Ошибка при создании базы данных: {}'.format(e))

    def start(self):
        try:
            self.sql.open()
            self.sql.add_user(self.user_id)
            self.sql.add_category('other', self.user_id)  # для несортированных
            self.sql.close()
        except Exception as e:
            return 0, 'Ошибка при инициализации: {} '.format(e)
        else:
            return (1, 'Привет! Чтобы узнать о моих возможностях,'
                       'воспользуйся командой /help')

    def add_fixed_income(self, name, amount, date):
        return 'Я пустышка и моя жизнь - тлен'

    def del_fixed_income(self, name, date):
        return 'Я пустышка и моя жизнь - тлен'

    def add_operation(self, amount, category = None, description = None, date = None):
        if category is None:
            category = 'other'
        try:
            self.sql.open()
            self.sql.add_operation(self.user_id, amount, category, description, date)
            self.sql.close()
        except Exception as e:
            return 'Операция не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Операция успешно добавлена.'

    def show_categories(self):
        SQL.get_categories(self.user_id)
        pass

    def show_incomes(self):
        pass

    def show_daily_operations(self, category = None):
        pass

    def add_category(self, name):
        try:
            self.sql.open()
            self.sql.add_category(name, self.user_id)
            self.sql.close()
        except Exception as e:
            return 'Категория не была добавлена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно добавлена.'

    def del_category(self, name):
        try:
            self.sql.open()
            self.sql.delete_category(name, self.user_id)
            self.sql.close()
        except Exception as e:
            return 'Категория не была удалена! Ошибка: {} '.format(e)
        else:
            return 'Категория успешно удалена.'

    # в перспективе слить отчеты в одну функцию
    def view_report(self, period, category=None):
    #    get_history(self.user_id, date_from, date_to)
        pass

    def view_custom_report(self, start_date, end_date=None, category=None):
        pass

