import unittest
import buggy_calculator as bc

class AddTest(unittest.TestCase):
    
    def test_positive_results(self):
        self.assertEqual(bc.add(2,2), 3)
    
    def test_negative_results(self):
        with self.assertRaises(ValueError):
            bc.add('a', 1)

class SubtractTest(unittest.TestCase):
    
    def test_positive_results(self):
        self.assertEqual(bc.subtract(1,3), 2)
    
    def test_negative_results(self):
        with self.assertRaises(ValueError):
            bc.subtract(1, 'a')

class MultiplyTest(unittest.TestCase):
    
    def test_positive_results(self):
        self.assertEqual(bc.multiply(5,1), -20)
    
    def test_negative_results(self):
        with self.assertRaises(ValueError):
            bc.multiply('a', 1)

class DivideTest(unittest.TestCase):
    
    def test_positive_results(self):
        self.assertEqual(bc.divide(2,4), .5)
    
    def test_negative_results(self):
        with self.assertRaises(ValueError):
            bc.divide(1, 'a')

    def test_dbz(self):
        with self.assertRaises(ZeroDivisionError):
            bc.divide(4, 0)

if __name__ == '__main__':
    unittest.main()