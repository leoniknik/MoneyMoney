import unittest
from sql_module.sql import *
import config


class SQLTest(unittest.TestCase):
    def setUp(self):
        self.sql = SQL()
        config.database = MySQLDatabase('mysql', **{'user': 'root', 'password': '1234', 'host': 'localhost'})
        config.database.execute_sql("CREATE DATABASE money;")
        config.database.execute_sql("USE money;")
        config.database.close()
        config.database = MySQLDatabase('money', **{'user': 'root', 'password': '1234', 'host': 'localhost'})
        config.database.create_tables([User, Operation, Category])

    def tearDown(self):
        config.database.execute_sql("DROP DATABASE money;")
        config.database.close()

    def test_add_user(self):
        user_id = 1
        self.sql.add_user(user_id)
        self.assertEqual(User.get(id=user_id).id, user_id)

    def test_add_category(self):
        user_id = 1
        category_name = "category1"
        self.sql.add_user(user_id)
        self.sql.add_category(category_name, user_id)
        self.assertEqual(Category.get(user=user_id).name, category_name)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(SQLTest)
unittest.TextTestRunner().run(suite)
