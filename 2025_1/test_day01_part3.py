import unittest
from day01_part3 import eni_sum_remainders, parse_line, compute_highest_sum_remainders
import os

class TestEnigmatusDay01Part3(unittest.TestCase):
    def test_eni_sum_remainders_examples(self):
        # Simple examples
        self.assertEqual(eni_sum_remainders(2, 7, 5), 18)  # 2^1 % 5 = 2, 2^2 % 5 = 4, ...
        self.assertEqual(eni_sum_remainders(3, 4, 7), 12)  # 3, 2, 6, 4
        self.assertEqual(eni_sum_remainders(5, 3, 13), 8)  # 5, 12, 8

    def test_parse_line(self):
        line = 'A=4 B=4 C=6 X=3 Y=14 Z=15 M=11'
        self.assertEqual(parse_line(line), (4, 4, 6, 3, 14, 15, 11))

    def test_compute_highest_sum_remainders(self):
        # Prepare a small test file
        test_input = "A=2 B=3 C=5 X=7 Y=4 Z=3 M=10\nA=4 B=4 C=6 X=3 Y=14 Z=15 M=11\n"
        test_file = os.path.join(os.path.dirname(__file__), "test_input_p3.txt")
        with open(test_file, 'w') as f:
            f.write(test_input)
        result = compute_highest_sum_remainders(test_file)
        self.assertTrue(isinstance(result, int))
        os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
