import unittest
from unittest import result
import calc


class TestCalc(unittest.TestCase):

    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)

    def test_subtract(self):
        self.assertEqual(calc.subtract(10, 5), 5)
        self.assertEqual(calc.subtract(50, 49), 1)
        self.assertEqual(calc.subtract(20, 10), 10)

    def test_multiply(self):
        self.assertEqual(calc.multiply(10, 5), 50)
        self.assertEqual(calc.multiply(20, 5), 100)
        self.assertEqual(calc.multiply(25, 4), 100)

    def test_divide(self):
        self.assertEqual(calc.divide(10, 5), 2)
        self.assertEqual(calc.divide(20, 5), 4)
        self.assertEqual(calc.divide(5, 2), 2)

        with self.assertRaises(ValueError):
            calc.divide(10, 0)


if __name__ == '__main__':
    unittest.main()
