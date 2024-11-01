"""import unittest
def divide(x,y):
    return x /y

class TestCalc(unittest.TestCase):
    def test_f(self):
        #self.assertEqual(self.divide(5,0),15)
        #self.assertRaises(ZeroDivisionError,divide,10,0)

        with self.assertRaises(ZeroDivisionError):
            divide(5,0)
if __name__ == '__main__':
    unittest.main()
    """
import unittest

class TestListContains(unittest.TestCase):
    def test_value_in_list(self):
        sample_list = [1, 2, 3, 4, 5]
        value = 7
        self.assertIn(value, sample_list, "Value not found in the list")

if __name__ == '__main__':
    unittest.main()