from sql import SQL

"""
MoneyMoney handler for all calculating functions.
List of functions:
add_fixed_income(name, amount, date)
add_income(amount, name)
add_expense(amount, category)
show_categories()
show_incomes()
show_daily_operations(category = None)
add_category(name)
del_category(name)
view_report(period, category = None)
view_custom_report(start_date, end_date = None, category = None)

"""


class MmHandler:
    def __init__(self, user_id):
        self.user_id = user_id

    def start(self):
        try:
            SQL.add_user(self.user_id)
            SQL.add_category('other', self.user_id)  # для несортированных расходов
            SQL.add_category('income', self.user_id) # для доходов
            SQL.add_category('fixed_income', self.user_id)  # для постоянных доходов
        except Exception:
            print("Unsuccessful, undefined error")
            return 0
        else:
            return 1

    def add_fixed_income(self, name, amount, date):
        # SQL.add_constant_operation(self.user_id, amount, name, date)
        pass

    def del_fixed_income(self, name, amount, date):
       # SQL.delete_constant_operation(self.user_id, amount, description)
        pass

    # в перспективе слить доход\расход в одну ф-ию
    def add_income(self, amount, name):
        pass

    def add_expense(self, amount, category):
        pass

    def show_categories(self):
     #   SQL.get_categories(self.user_id)
        pass

    def show_incomes(self):
        pass

    def show_daily_operations(self, category=None):
        pass

    def add_category(self, name):
    #    SQL.add_category(self, name, self.user_id)
        pass

    def del_category(self, name):
    #    SQL.delete_category(name, self.user_id)
        pass

    # в перспективе слить отчеты в одну функцию
    def view_report(self, period, category=None):
    #    get_history(self.user_id, date_from, date_to)
        pass

    def view_custom_report(self, start_date, end_date=None, category=None):
        pass
