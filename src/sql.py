import MySQLdb
import datetime


class SQL:
    unnamed_category = "unnamed"
    db = None
    cursor = None

    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.passwd = "1234"
        self.database = "money"
        self.charset = 'utf8'

    def open(self):
        # соединяемся с базой данных
        self.db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.database, charset=self.charset)
        # формируем курсор
        self.cursor = self.db.cursor()

    def close(self):
        # закрываем соединение
        self.db.close()

    def _execute_query(self, sql_query):
        # выполняем запрос
        self.cursor.execute(sql_query)
        # применяем изменения к базе данных
        self.db.commit()
        # получаем результат выполнения запроса
        data = self.cursor.fetchall()
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

    def get_expense_categories(self,user_id):
        sql_query = "SELECT name FROM category WHERE user_id = {};".format(user_id)
        data = self._execute_query(sql_query)
        result = list()
        for item in data:
            result.append(item[0])
        return result

    def get_income_categories(self,user_id):
        sql_query = "SELECT name FROM category WHERE user_id = {};".format(user_id)
        data = self._execute_query(sql_query)
        result = list()
        for item in data:
            result.append(item[0])
        return result

    def add_category(self, category_name, user_id):
        data = self.get_all_categories(user_id)
        if category_name not in data:
            sql_query = "INSERT INTO category (name, user_id) VALUES (\"{}\", {});".format(category_name, user_id)
            self._execute_query(sql_query)

    def delete_category(self, category_name, user_id):
        data = self.get_all_categories(user_id)
        if category_name in data:
            sql_query = "DELETE FROM category WHERE name=\"{}\" and user_id={};".format(category_name, user_id)
            self._execute_query(sql_query)
            self._rename_category_after_delete(category_name, user_id)

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
        if SQL.unnamed_category not in data:
            self.add_category(SQL.unnamed_category, user_id)
        id_category = self._get_category_id(user_id, SQL.unnamed_category)
        return id_category

    def add_operation(self, user_id, amount, description=None, date=None, category=None):
        if description is None:
            description = ""
        if date is None:
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        if category is None:
            self._add_unnamed_category(user_id)
            id_category = self._get_category_id(user_id, SQL.unnamed_category)
        else:
            id_category = self._get_category_id(user_id, category)
        sql_query = "INSERT INTO operation (sum, date, id_user, id_cat, description) VALUES ({}, \"{}\", {}, {}, \"{}\");" \
            .format(amount, date, user_id, id_category, description)
        self._execute_query(sql_query)

    # пока просто возвращает list сумм всех операций за период по всем категориям
    def get_history(self, user_id, date_from, date_to=None):
        if datetime.datetime.strptime(date_to, "%Y-%m-%d") > datetime.datetime.now():
            date_to = datetime.datetime.now().strftime("%Y-%m-%d")
        if date_to is None:
            date_to = datetime.datetime.now().strftime("%Y-%m-%d")
        sql_query = "SELECT sum, description FROM operation WHERE date BETWEEN \"{}\" AND \"{}\" AND id_user={};" \
            .format(date_from, date_to, user_id)
        data = self._execute_query(sql_query)
        return data
