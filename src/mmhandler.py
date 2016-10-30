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
        pass
    
    def add_fixed_income(name, amount, date):
        pass
    
    # в перспективе слить доход\расход в одну ф-ию
    def add_income(amount, name):
        pass
    def add_expense(amount, category):
        pass
    
    def show_categories():
        pass
    def show_incomes():
        pass
    def show_daily_operations(category = None):
        pass
    
    def add_category(name):
        pass
    def del_category(name):
        pass
    
    # в перспективе слить отчеты в одну функцию
    def view_report(period, category = None):
        pass
    def view_custom_report(start_date, end_date = None, category = None):
        pass
   
