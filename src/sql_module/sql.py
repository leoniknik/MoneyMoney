import datetime
from sql_module.models import *
from sql_module.sql_exception import *
import logging
from raven import Client

client = Client('https://4724d5de1d92423f95ccfc2010f0b138:f4cc360abbd24bda9db016fa99b14145@sentry.io/120805')
logging.basicConfig(format=u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.DEBUG, filename=u'database.log')


class SQL:
    _other_category = "other"
    _unused_category_type = 0
    _income_category_type = 1
    _expense_category_type = 2
    _general_category_type = 3

    def add_user(self, user_id):
        try:
            User.create(id=user_id)
            logging.info("Был добавлен пользователь с id=" + str(user_id))
        except Exception:
            client.captureException()
            raise UserAlreadyExist

    def add_category(self, category_name, user_id):
        try:
            Category.get(user=user_id, name=category_name)
        except Exception:
            Category.create(user=user_id, name=category_name, type=SQL._unused_category_type)
            logging.info("Была добавлена категория=" + str(category_name) + " для пользвателя с id=" + str(user_id))
        else:
            raise CategoryExistException

    def get_all_categories(self, user_id):
        result = list()
        for item in Category.select().where(Category.user == user_id):
            result.append(item.name)
        if len(result) == 0:
            raise CategoriesNotExist
        logging.info("Были получены все категории для пользователя с id=" + str(user_id))
        return result

    def get_expense_categories(self, user_id):
        result = list()
        for item in Category.select().where(Category.user == user_id, (Category.type == SQL._general_category_type) | (
                    Category.type == SQL._expense_category_type)):
            result.append(item.name)
        if len(result) == 0:
            raise ExpenseCategoriesNotExist
        logging.info("Были получены категории расходов для пользователя с id=" + str(user_id))
        return result

    def get_income_categories(self, user_id):
        result = list()
        for item in Category.select().where(Category.user == user_id, (Category.type == SQL._general_category_type) | (
                    Category.type == SQL._income_category_type)):
            result.append(item.name)
        if len(result) == 0:
            raise IncomeCategoriesNotExist
        logging.info("Были получены категории доходов для пользователя с id=" + str(user_id))
        return result

    def delete_category(self, category_name, user_id):
        data = self.get_all_categories(user_id)
        if category_name in data:
            self._rename_category_after_delete(category_name, user_id)
            Category.delete().where(Category.user == user_id, Category.name == category_name).execute()
            logging.info("Была удалена категория=" + str(category_name) + " для пользвателя с id=" + str(user_id))
        else:
            raise CategoryNotExistException

    def _rename_category_after_delete(self, category_name, user_id):
        try:
            id_replaceable_category = self._get_category_id(user_id, category_name)
            id_other_category = self._get_category_id(user_id)
            Operation.update(id_cat=id_other_category).where(Operation.id_cat == id_replaceable_category,
                                                             Operation.id_user == user_id).execute()
            logging.info("Операции категории=" + str(
                category_name) + " переместились в категорию other для пользвателя с id=" + str(user_id))
        except Exception:
            client.captureException()

    def _get_category_id(self, user_id, category_name=None):
        try:
            if category_name is None:
                data = self.get_all_categories(user_id)
                if SQL._other_category not in data:
                    self.add_category(SQL._other_category, user_id)
                category_id = Category.get(user=user_id, name=SQL._other_category).id
            else:
                category_id = Category.get(user=user_id, name=category_name).id
            return category_id
        except Exception:
            self.add_category(SQL._other_category, user_id)
            category_id = Category.get(user=user_id, name=SQL._other_category).id
            return category_id


    def add_operation(self, user_id, amount, category=None, date=None, description=None):
        try:
            if description is None:
                description = ""
            if date is None:
                date = datetime.datetime.now().strftime("%Y-%m-%d")
            id_category = self._get_category_id(user_id, category)
            category_type = SQL._change_category_type(self._get_category_type(id_category), amount)
            Category.update(type=category_type).where(Category.id == id_category).execute()
            Operation.create(amount=amount, date=date, id_cat=id_category, id_user=user_id, description=description,
                             type=category_type)
            logging.info(
                "Была добавлена операция на сумму=" + str(amount) + " для категории=" + str(
                    category) + " с описанием=" + str(description) + " с датой=" + str(
                    date) + " для пользователя с id=" + str(user_id))
        except Exception:
            client.captureException()

    def get_history(self, user_id, date_from=None, date_to=None):
        result = list()
        date_now = datetime.date.today()
        if date_from is None and date_to is None:
            data = Operation.select().where(Operation.id_user == user_id)
            for item in data:
                name = self._get_category_name(item.id_cat)
                result.append([item.amount, name, str(item.date), item.description ])
        else:
            date_from = datetime.datetime.strptime(date_from, "%Y-%m-%d").date()
            if date_to is None:
                date_to = date_now
            else:
                date_to = datetime.datetime.strptime(date_to, "%Y-%m-%d").date()
            data = Operation.select().where(Operation.id_user == user_id,
                                            (Operation.date >= date_from) & (Operation.date <= date_to))
            for item in data:
                name = self._get_category_name(item.id_cat)
                result.append([item.amount, name, str(item.date), item.description])
        if len(result) == 0:
            raise HistoryNotExist
        logging.info(
            "Был создан отчет для пользователя с id=" + str(user_id) + " от даты=" + str(date_from) + " по дату=" + str(
                date_to))
        return result

    def _get_category_type(self, id_category):
        try:
            category_type = Category.get(id=id_category).type
            return category_type
        except Exception:
            client.captureException()

    @staticmethod
    def _change_category_type(category_type, amount):
        try:
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
        except Exception:
            client.captureException()

    #тут не надо оберега, мы у себя
    def delete_category_other(self, user_id):
        id = self._get_category_id(user_id)
        Operation.delete().where(Operation.id_user == user_id, Operation.id_cat == id).execute()
        self.delete_category(SQL._other_category,user_id)

    def _get_category_name(self, id_cat):
        name = Category.get(id=id_cat).name
        return name

sql = SQL()
list = sql.get_history(224634311)
pass