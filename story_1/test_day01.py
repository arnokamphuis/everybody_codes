import unittest
from day01 import eni, parse_line, compute_highest_sum
import os

class TestEnigmatusDay01(unittest.TestCase):
    def test_eni_examples(self):
        # Examples from the story
        self.assertEqual(eni(2, 4, 5), 1342)
        self.assertEqual(eni(3, 5, 16), 311193)
        self.assertEqual(eni(4, 3, 11), 954)
        self.assertEqual(eni(4, 4, 11), 3954)
        self.assertEqual(eni(6, 5, 11), 109736)

    def test_parse_line(self):
        line = 'A=2 B=8 C=5 X=7 Y=4 Z=5 M=20'
        self.assertEqual(parse_line(line), (2, 8, 5, 7, 4, 5, 20))

    def test_compute_highest_sum(self):
        # Prepare a small test file
        test_input = "A=2 B=8 C=5 X=7 Y=4 Z=5 M=20\nA=3 B=3 C=7 X=3 Y=5 Z=6 M=26\n"
        test_file = os.path.join(os.path.dirname(__file__), "test_input.txt")
        with open(test_file, 'w') as f:
            f.write(test_input)
        result = compute_highest_sum(test_file)
        self.assertTrue(isinstance(result, int))
        os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
