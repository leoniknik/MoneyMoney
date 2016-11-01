import MySQLdb
import datetime


class SQL:
    _unnamed_category = "unnamed"
    _unused_category_type = 0
    _income_category_type = 1
    _expense_category_type = 2
    _general_category_type = 3
    _db = None
    _cursor = None

    def __init__(self):
        self._host = "localhost"
        self._user = "root"
        self._passwd = "1234"
        self._database = "money"
        self._charset = 'utf8'

    def open(self):
        # соединяемся с базой данных
        self._db = MySQLdb.connect(host=self._host, user=self._user, passwd=self._passwd, db=self._database, charset=self._charset)
        # формируем курсор
        self._cursor = self._db.cursor()

    def close(self):
        # закрываем соединение
        self._db.close()

    def _execute_query(self, sql_query):
        # выполняем запрос
        self._cursor.execute(sql_query)
        # применяем изменения к базе данных
        self._db.commit()
        # получаем результат выполнения запроса
        data = self._cursor.fetchall()
        return data

    def add_user(self, user_id):
        sql_query = "INSERT INTO user (id) VALUES ({});".format(user_id)
        self._execute_query(sql_query)

    # возвращает list
    def get_all_categories(self, user_id):
        sql_query = "SELECT name FROM category WHERE user_id = {};".format(user_id)
        data = self._execute_query(sql_query)
        result = list()
        for item in data:
            result.append(item[0])
        return result

    def get_expense_categories(self, user_id):
        sql_query = "SELECT name FROM category WHERE user_id = {} and type IN ({},{});"\
            .format(user_id, SQL._expense_category_type, SQL._general_category_type)
        data = self._execute_query(sql_query)
        result = list()
        for item in data:
            result.append(item[0])
        return result

    def get_income_categories(self, user_id):
        sql_query = "SELECT name FROM category WHERE user_id = {} and type IN ({},{});"\
            .format(user_id, SQL._income_category_type, SQL._general_category_type)
        data = self._execute_query(sql_query)
        result = list()
        for item in data:
            result.append(item[0])
        return result

    def add_category(self, category_name, user_id):
        data = self.get_all_categories(user_id)
        if category_name not in data:
            sql_query = "INSERT INTO category (name, user_id, type) VALUES (\"{}\", {}, {});"\
                .format(category_name, user_id, SQL._unused_category_type)
            self._execute_query(sql_query)

    def delete_category(self, category_name, user_id):
        data = self.get_all_categories(user_id)
        if category_name in data:
            sql_query = "DELETE FROM category WHERE name=\"{}\" and user_id={};".format(category_name, user_id)
            self._rename_category_after_delete(category_name, user_id)
            self._execute_query(sql_query)

    def _rename_category_after_delete(self, category_name, user_id):
        id_replaceable_category = self._get_category_id(user_id, category_name)
        id_unnamed_category = self._get_unnamed_category_id(user_id)
        sql_query = "UPDATE operation SET id_cat={} WHERE id_cat={} and user_id={};" \
            .format(id_unnamed_category, id_replaceable_category, user_id)
        self._execute_query(sql_query)

    # возвращает int
    def _get_category_id(self, user_id, category_name):
        sql_query = "SELECT id FROM category WHERE user_id={} and name=\"{}\";".format(user_id, category_name)
        category_id = self._execute_query(sql_query)
        return category_id[0][0]

    def _get_unnamed_category_id(self, user_id):
        data = self.get_all_categories(user_id)
        if SQL._unnamed_category not in data:
            self.add_category(SQL._unnamed_category, user_id)
        id_category = self._get_category_id(user_id, SQL._unnamed_category)
        return id_category

    def add_operation(self, user_id, amount, description=None, date=None, category=None):
        if description is None:
            description = ""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        if category is None:
            self.add_category(SQL._unnamed_category, user_id)
            id_category = self._get_category_id(user_id, SQL._unnamed_category)
        else:
            id_category = self._get_category_id(user_id, category)
        category_type = SQL._change_category_type(self._get_category_type(id_category), amount)
        sql_query = "INSERT INTO operation (sum, date, id_user, id_cat, description, type) VALUES ({}, \"{}\", {}, {}, \"{}\", {});"\
            .format(amount, date, user_id, id_category, description, category_type)
        self._execute_query(sql_query)

    # пока просто возвращает list сумм всех операций за период по всем категориям
    def get_history(self, user_id, date_from=None, date_to=None):
        if date_from is None and date_to is None:
            sql_query = "SELECT sum, description FROM operation WHERE id_user={}".format(user_id)
        else:
            if datetime.datetime.strptime(date_to, "%Y-%m-%d") > datetime.datetime.now():
                date_to = datetime.datetime.now().strftime("%Y-%m-%d")
            if date_to is None:
                date_to = datetime.datetime.now().strftime("%Y-%m-%d")
            sql_query = "SELECT sum, description FROM operation WHERE date BETWEEN \"{}\" AND \"{}\" AND id_user={};"\
                .format(date_from, date_to, user_id)
        data = self._execute_query(sql_query)
        return data

    def _get_category_type(self, id_category):
        sql_query = "SELECT type FROM category WHERE id_cat={};".format(id_category)
        category_type = self._execute_query(sql_query)
        return category_type[0][0]

    @staticmethod
    def _change_category_type(category_type, amount):
        if category_type == SQL._unused_category_type:
            if amount > 0:
                category_type = SQL._income_category_type
            elif amount < 0:
                category_type = SQL._expense_category_type
        elif category_type == SQL._income_category_type:
            if amount < 0:
                category_type == SQL._general_category_type
        elif category_type == SQL._expense_category_type:
            if amount > 0:
                category_type = SQL._general_category_type
        return category_type
