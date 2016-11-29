import datetime
from models import *
from sql_exception import *


class SQL:
    _other_category = "other"
    _unused_category_type = 0
    _income_category_type = 1
    _expense_category_type = 2
    _general_category_type = 3

    def add_user(self, user_id):
        try:
            User.create(id=user_id)
        except:
            raise UserAlreadyExist

    def add_category(self, category_name, user_id):
        try:
            Category.get(user=user_id, name=category_name)
        except Exception:
            Category.create(user=user_id, name=category_name, type=SQL._unused_category_type)
        else:
            raise CategoryExistException

    def get_all_categories(self, user_id):
        result = list()
        for item in Category.select().where(Category.user == user_id):
            result.append(item.name)
        if len(result) == 0:
            raise CategoriesNotExist
        return result

    def get_expense_categories(self, user_id):
        result = list()
        for item in Category.select().where(Category.user == user_id, (Category.type == SQL._general_category_type) | (Category.type == SQL._expense_category_type)):
            result.append(item.name)
        if len(result) == 0:
            raise ExpenseCategoriesNotExist
        return result

    def get_income_categories(self, user_id):
        result = list()
        for item in Category.select().where(Category.user == user_id, (Category.type == SQL._general_category_type) | (Category.type == SQL._income_category_type)):
            result.append(item.name)
        if len(result) == 0:
            raise IncomeCategoriesNotExist
        return result

    def delete_category(self, category_name, user_id):
        data = self.get_all_categories(user_id)
        if category_name in data:
            self._rename_category_after_delete(category_name, user_id)
            Category.delete().where(Category.user == user_id, Category.name == category_name).execute()
        else:
            raise CategoryNotExistException

    def _rename_category_after_delete(self, category_name, user_id):
        id_replaceable_category = self._get_category_id(user_id, category_name)
        id_other_category = self._get_category_id(user_id)
        Operation.update(id_cat=id_other_category).where(Operation.id_cat == id_replaceable_category, Operation.id_user == user_id).execute()

    def _get_category_id(self, user_id, category_name=None):
        if category_name is None:
            data = self.get_all_categories(user_id)
            if SQL._other_category not in data:
                self.add_category(SQL._other_category, user_id)
            category_id = Category.get(user=user_id, name=SQL._other_category).id
        else:
            category_id = Category.get(user=user_id, name=category_name).id
        return category_id

    def add_operation(self, user_id, amount, category=None, date=None, description=None):
        if description is None:
            description = ""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        id_category = self._get_category_id(user_id, category)
        category_type = SQL._change_category_type(self._get_category_type(id_category), amount)
        Category.update(type=category_type).where(Category.id == id_category).execute()
        Operation.create(amount=amount, date=date, id_cat=id_category, id_user=user_id, description=description, type=category_type)

    def get_history(self, user_id, date_from=None, date_to=None):
        result = list()
        date_now = datetime.date.today()
        if date_from is None and date_to is None:
            data = Operation.select().where(Operation.id_user == user_id)
            for item in data:
                result.append([item.amount, item.description])
        else:
            date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
            if date_to is None:
                date_to = date_now
            data = Operation.select().where(Operation.id_user == user_id,(Operation.date >= date_from)&(Operation.date <= date_to))
            for item in data:
                result.append([item.amount, item.description])
        if len(result) == 0:
            raise HistoryNotExist
        return result

    def _get_category_type(self, id_category):
        category_type = Category.get(id=id_category).type
        return category_type

    @staticmethod
    def _change_category_type(category_type, amount):
        if category_type == SQL._unused_category_type:
            if amount > 0:
                category_type = SQL._income_category_type
            elif amount < 0:
                category_type = SQL._expense_category_type
        elif category_type == SQL._income_category_type:
            if amount < 0:
                category_type = SQL._general_category_type
        elif category_type == SQL._expense_category_type:
            if amount > 0:
                category_type = SQL._general_category_type
        return category_type
