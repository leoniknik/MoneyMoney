import unittest


class SQL_Test(unittest.TestCase):
    def setUp(self):
        self.sql = SQL()

    def test_add(self):
        self.alchemy.add(Item("C"))
        self.alchemy.add(Item("F"))
        self.assertEqual(len(self.alchemy.items), 2)

    def test_remove(self):
        item = Item("C")
        self.alchemy.add(item)
        self.assertEqual(len(self.alchemy.items), 1)
        self.alchemy.remove(item)
        self.assertEqual(len(self.alchemy.items), 0)

    def test_boom(self):
        item1 = Item("Na", reacts_with=["H2O"])
        item2 = Item("H2O", reacts_with=["Na"])
        self.alchemy.add(item1)
        self.assertRaises(BoomException, self.alchemy.add, item2)
        self.assertEqual(len(self.alchemy.items), 0)


# Обычно в реальных проектах использует механизм автоматического нахождения тестов (discover).
suite = unittest.defaultTestLoader.loadTestsFromTestCase(AlchemyTest)
unittest.TextTestRunner().run(suite)
