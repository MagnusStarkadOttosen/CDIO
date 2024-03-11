import unittest
from testing import *
from src.client.pathFinder import are_balls_remaining



class MyTestCase(unittest.TestCase):

    def are_balls_remaining(self):
        expected =True
        actual= are_balls_remaining(self)
        self.assertEqual(expected, actual)  # add assertion here


if __name__ == '__main__':
    unittest.main()
