import unittest

# This is the function we want to test
# (In a real project, you would import this: from src.math_utils import add)
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

class TestMathOperations(unittest.TestCase):

    def test_add(self):
        """Test if the add function correctly sums two numbers."""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_divide(self):
        """Test if the divide function works correctly."""
        self.assertEqual(divide(10, 2), 5)
        self.assertAlmostEqual(divide(10, 3), 3.3333, places=4)

    def test_divide_by_zero(self):
        """Test if dividing by zero raises a ValueError."""
        with self.assertRaises(ValueError):
            divide(10, 0)

if __name__ == '__main__':
    unittest.main()
