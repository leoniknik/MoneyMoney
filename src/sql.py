import MySQLdb
import datetime


class SQL:
    host = "localhost"
    user = "root"
    passwd = "1234"
    database = "money"
    charset = 'utf8'

    const_category = "fixed"

    @classmethod
    def execute_query(cls, sql_query):
        # соединяемся с базой данных
        db = MySQLdb.connect(host=cls.host, user=cls.user, passwd=cls.passwd, db=cls.database, charset=cls.charset)
        # формируем курсор
        cursor = db.cursor()
        # выполняем запрос
        cursor.execute(sql_query)
        # применяем изменения к базе данных
        db.commit()
        # получаем результат выполнения запроса
        data = cursor.fetchall()
        db.close()
        return data

    @staticmethod
    def add_user(user_id):
        sql_query = "INSERT INTO user (id) VALUES ({});".format(user_id)
        SQL.execute_query(sql_query)

    #возвращает list
    @staticmethod
    def get_categories(user_id):
        sql_query = "SELECT name FROM category WHERE user_id = {};".format(user_id)
        data = SQL.execute_query(sql_query)
        result = list()
        for item in data:
            result.append(item[0])
        return result

    @staticmethod
    def add_category(category_name, user_id):
        data = SQL.get_categories(user_id)
        for item in data:
            if item == category_name:
                return
        sql_query = "INSERT INTO category (name, user_id) VALUES (\"{}\", {});".format(category_name, user_id)
        SQL.execute_query(sql_query)

    @staticmethod
    def delete_category(category_name, user_id):
        data = SQL.get_categories(user_id)
        if category_name in data:
            sql_query = "DELETE FROM category WHERE name=\"{}\" and user_id={};".format(category_name, user_id)
            SQL.execute_query(sql_query)

    #возвращает int
    @staticmethod
    def get_category_id(user_id, name):
        sql_query = "SELECT id FROM category WHERE user_id={} and name=\"{}\";".format(user_id, name)
        category_id = SQL.execute_query(sql_query)
        return category_id[0][0]

    @staticmethod
    def add_constant_operation(user_id, sum, description):
        data = SQL.get_categories(user_id)
        if SQL.const_category not in data:
            SQL.add_category(SQL.const_category, user_id)
        id_category = SQL.get_category_id(user_id, SQL.const_category)
        data_now = datetime.datetime.now().strftime("%Y-%m-%d")
        sql_query = "INSERT INTO operation (sum, date, id_user, id_cat, description) VALUES ({}, \"{}\", {}, {}, \"{}\");" \
            .format(sum, data_now, user_id, id_category, description)
        SQL.execute_query(sql_query)

    @staticmethod
    def delete_constant_operation():
        pass  # все-таки вопрос как хранить в бд постоянные доходы, т.е. как определять что они постоянные и как пользователь будет добавлять/удалять их

    @staticmethod
    def add_operation(user_id, sum, category, description):
        id_category = SQL.get_category_id(user_id, category)
        data_now = datetime.datetime.now().strftime("%Y-%m-%d")
        sql_query = "INSERT INTO operation (sum, date, id_user, id_cat, description) VALUES ({}, \"{}\", {}, {}, \"{}\");" \
            .format(sum, data_now, user_id, id_category, description)
        SQL.execute_query(sql_query)

    # пока просто возвращает list сумм всех операций за период по всем категориям
    @staticmethod
    def get_history(user_id, date_from, date_to):
        if datetime.datetime.strptime(date_to, "%Y-%m-%d") > datetime.datetime.now():
            date_to = datetime.datetime.now().strftime("%Y-%m-%d")
        sql_query = "SELECT sum, description FROM operation WHERE date BETWEEN \"{}\" AND \"{}\" AND id_user={};" \
            .format(date_from, date_to, user_id)
        data = SQL.execute_query(sql_query)
        return data
    
