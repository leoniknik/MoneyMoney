import os, sys

import unittest
from src.sql_module.sql import *


class SQLTest(unittest.TestCase):
    def setUp(self):
        self.sql = SQL()
        self.database = MySQLDatabase('mysql', **{'user': 'root', 'password': '7uy33HZ5', 'host': 'localhost'})
        self.database.execute_sql("CREATE DATABASE money;")
        self.database.execute_sql("USE money;")
        self.database.close()
        self.database = MySQLDatabase('money', **{'user': 'root', 'password': '7uy33HZ5', 'host': 'localhost'})
        self.database.create_tables([User, Operation, Category])

    def tearDown(self):
        self.database.execute_sql("DROP DATABASE money;")
        self.database.close()

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
