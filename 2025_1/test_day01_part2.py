import unittest
from day01_part2 import eni_truncated, parse_line, compute_highest_sum_truncated
import os

class TestEnigmatusDay01Part2(unittest.TestCase):
    def test_eni_truncated_examples(self):
        # Examples from the story
        self.assertEqual(eni_truncated(2, 7, 5), 34213)
        self.assertEqual(eni_truncated(3, 8, 16), 111931)
        self.assertEqual(eni_truncated(4, 3, 11), 954)
        self.assertEqual(eni_truncated(4, 14, 11), 39541)
        self.assertEqual(eni_truncated(6, 15, 11), 109736)

    def test_parse_line(self):
        line = 'A=4 B=4 C=6 X=3 Y=14 Z=15 M=11'
        self.assertEqual(parse_line(line), (4, 4, 6, 3, 14, 15, 11))

    def test_compute_highest_sum_truncated(self):
        # Prepare a small test file
        test_input = "A=4 B=4 C=6 X=3 Y=14 Z=15 M=11\nA=8 B=4 C=7 X=8 Y=14 Z=16 M=12\n"
        test_file = os.path.join(os.path.dirname(__file__), "test_input_p2.txt")
        with open(test_file, 'w') as f:
            f.write(test_input)
        result = compute_highest_sum_truncated(test_file)
        self.assertTrue(isinstance(result, int))
        os.remove(test_file)

if __name__ == "__main__":
    unittest.main()
