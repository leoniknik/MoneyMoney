import MySQLdb


class SQL:
    host = "localhost"
    user = "root"
    passwd = "1234"
    database = "my"
    charset = 'utf8'

    @classmethod
    def add_profit(cls):
        # соединяемся с базой данных
        db = MySQLdb.connect(host=cls.host, user=cls.user, passwd=cls.passwd, db=cls.database, charset=cls.charset)
        # формируем курсор
        cursor = db.cursor()
        # запрос к БД
        sql = """SELECT * FROM user;"""
        # выполняем запрос
        cursor.execute(sql)
        # получаем результат выполнения запроса
        data = cursor.fetchall()
        # перебираем записи
        for rec in data:
            print(rec)
        # закрываем соединение с БД
        db.close()
