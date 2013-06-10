import unittest
from p import scan

class TestRobotScanner(unittest.TestCase):
    def test_disallow_first_raise_exception(self):
        with open('disallow-first.txt', 'r') as f:
            body = f.read()
        self.assertRaises(Exception, scan, body)

