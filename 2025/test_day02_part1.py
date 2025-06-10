import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from day02_part1 import parse_input, BinarySearchTree, build_trees, get_message_from_trees

class TestParseInput(unittest.TestCase):
    def test_parse_input(self):
        # Use a small test file
        test_file = os.path.join(os.path.dirname(__file__), "input", "everybody_codes_e1_q02_p1.txt")
        left, right = parse_input(test_file)
        self.assertIsInstance(left, list)
        self.assertIsInstance(right, list)
        self.assertTrue(all(isinstance(x, tuple) and len(x) == 2 for x in left))
        self.assertTrue(all(isinstance(x, tuple) and len(x) == 2 for x in right))
        # Check that ranks are int and symbols are str
        self.assertTrue(all(isinstance(x[0], int) and isinstance(x[1], str) for x in left))
        self.assertTrue(all(isinstance(x[0], int) and isinstance(x[1], str) for x in right))

class TestBST(unittest.TestCase):
    def test_insert_and_level_order(self):
        bst = BinarySearchTree()
        nodes = [(10, 'A'), (15, 'B'), (5, 'C'), (12, 'D'), (20, 'E')]
        for rank, sym in nodes:
            bst.insert(rank, sym)
        levels = bst.level_order()
        self.assertEqual(levels[0], [(10, 'A')])
        self.assertEqual(set(levels[1]), set([(5, 'C'), (15, 'B')]))
        self.assertEqual(set(levels[2]), set([(12, 'D'), (20, 'E')]))

    def test_most_populated_level_symbols(self):
        bst = BinarySearchTree()
        nodes = [(10, 'A'), (15, 'B'), (5, 'C'), (12, 'D'), (20, 'E')]
        for rank, sym in nodes:
            bst.insert(rank, sym)
        # Level 1 has 2 nodes: C and B (left and right of root)
        self.assertEqual(set(bst.most_populated_level_symbols()), set(['C', 'B']))

class TestBuildTrees(unittest.TestCase):
    def test_build_trees(self):
        left_nodes = [(10, 'A'), (5, 'B'), (15, 'C')]
        right_nodes = [(20, 'X'), (25, 'Y'), (18, 'Z')]
        left_tree, right_tree = build_trees(left_nodes, right_nodes)
        self.assertEqual(left_tree.root.rank, 10)
        self.assertEqual(left_tree.root.left.rank, 5)
        self.assertEqual(left_tree.root.right.rank, 15)
        self.assertEqual(right_tree.root.rank, 20)
        self.assertEqual(right_tree.root.left.rank, 18)
        self.assertEqual(right_tree.root.right.rank, 25)

class TestGetMessageFromTrees(unittest.TestCase):
    def test_get_message_from_trees(self):
        # Build two small trees
        left_nodes = [(10, 'A'), (5, 'B'), (15, 'C'), (3, 'D'), (7, 'E')]
        right_nodes = [(20, 'X'), (25, 'Y'), (18, 'Z'), (22, 'W'), (30, 'Q')]
        left_tree, right_tree = build_trees(left_nodes, right_nodes)
        msg = get_message_from_trees(left_tree, right_tree)
        # For left: level 1 has 2 nodes: B and C; for right: level 1 has 2 nodes: Z and Y
        self.assertEqual(set(msg), set(['B', 'C', 'Z', 'Y']))

class TestEndToEnd(unittest.TestCase):
    def test_end_to_end(self):
        # Use a small sample input
        left_nodes = [(10, 'A'), (5, 'B'), (15, 'C')]
        right_nodes = [(20, 'X'), (25, 'Y'), (18, 'Z')]
        left_tree, right_tree = build_trees(left_nodes, right_nodes)
        msg = get_message_from_trees(left_tree, right_tree)
        # For left: level 1 has 2 nodes: B and C; for right: level 1 has 2 nodes: Z and Y
        self.assertEqual(set(msg), set(['B', 'C', 'Z', 'Y']))

if __name__ == "__main__":
    unittest.main()
