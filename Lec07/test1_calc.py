import unittest
from unittest import result
import calc


class TestCalc(unittest.TestCase):

    def test_add(self):
        result = calc.add(10, 5)
        self.assertEqual(result, 15)
        # self.assertEqual(calc.add(10, 5), 15)
        # self.assertEqual(calc.add(-1, 1), 0)
        # self.assertEqual(calc.add(-1, 1), 15)


if __name__ == '__main__':
    unittest.main()
