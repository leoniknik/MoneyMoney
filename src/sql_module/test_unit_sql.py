from sql_module.sql import SQL
import unittest


class SQLTest(unittest.TestCase):
    def setUp(self):
        self.sql = SQL()

    def test_add_user(self):
        user_id = 1
        self.sql.execute_query("START TRANSACTION;")
        self.sql.add_user(user_id)
        self.assertEqual(self.sql.execute_query("SELECT id FROM user WHERE id={}".format(user_id))[0][0], 1)
        self.sql.execute_query("ROLLBACK;")
        self.sql.close()

suite = unittest.defaultTestLoader.loadTestsFromTestCase(SQLTest)
unittest.TextTestRunner().run(suite)
