import unittest
from mmhandler import MmHandler
from unittest.mock import patch, Mock


class TestStart(unittest.TestCase):

    def setUp(self):
        self.handler = MmHandler(0)

    @patch('db.add_user(self.user_id)', Mock(return_value=1))
    def test_add_user(self):
        self.assertEqual(self.handler.start(), (1, 'Привет! Чтобы узнать о моих возможностях,'
                       'воспользуйся командой /help'))



suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStart)
unittest.TextTestRunner().run(suite)
