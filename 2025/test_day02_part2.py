import unittest
import os
import sys
sys.path.insert(0, os.path.dirname(__file__))
from day02_part2 import parse_commands, BinarySearchTree

class TestParseCommands(unittest.TestCase):
    def test_parse_and_swap(self):
        """
        Test that parse_commands returns two lists (left_nodes, right_nodes).
        """
        import tempfile
        from day02_part2 import parse_commands
        lines = [
            "ADD id=1 left=[10,A] right=[20,X]",
            "ADD id=2 left=[5,B] right=[25,Y]",
            "SWAP 1",
            "ADD id=3 left=[15,C] right=[18,Z]"
        ]
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            for line in lines:
                f.write(line + "\n")
            fname = f.name
        left_nodes, right_nodes = parse_commands(fname)
        self.assertIsInstance(left_nodes, list)
        self.assertIsInstance(right_nodes, list)
        self.assertEqual(left_nodes, [(20, 'X'), (5, 'B'), (15, 'C')])
        self.assertEqual(right_nodes, [(10, 'A'), (25, 'Y'), (18, 'Z')])

class TestBSTPart2(unittest.TestCase):
    def test_insert_and_level_order(self):
        """
        Test BST insertion and level-order traversal for Part II.
        """
        bst = BinarySearchTree()
        nodes = [(10, 'A'), (15, 'B'), (5, 'C'), (12, 'D'), (20, 'E')]
        for i, (rank, sym) in enumerate(nodes):
            bst.insert(rank, sym, str(i))
        levels = bst.level_order()
        self.assertEqual(levels[0], [(10, 'A')])
        self.assertEqual(set(levels[1]), set([(5, 'C'), (15, 'B')]))
        self.assertEqual(set(levels[2]), set([(12, 'D'), (20, 'E')]))

    def test_most_populated_level_symbols(self):
        """
        Test extracting symbols from the most populated level.
        """
        bst = BinarySearchTree()
        nodes = [(10, 'A'), (15, 'B'), (5, 'C'), (12, 'D'), (20, 'E')]
        for i, (rank, sym) in enumerate(nodes):
            bst.insert(rank, sym, str(i))
        self.assertEqual(set(bst.most_populated_level_symbols()), set(['C', 'B']))

    def test_build_trees(self):
        """
        Test building left and right BSTs from node lists.
        """
        from day02_part2 import build_trees, BinarySearchTree
        left_nodes = [(10, 'A'), (5, 'B'), (15, 'C')]
        right_nodes = [(20, 'X'), (25, 'Y'), (18, 'Z')]
        # Use dummy IDs for test
        left_tree = BinarySearchTree()
        for i, (rank, sym) in enumerate(left_nodes):
            left_tree.insert(rank, sym, f"L{i}")
        right_tree = BinarySearchTree()
        for i, (rank, sym) in enumerate(right_nodes):
            right_tree.insert(rank, sym, f"R{i}")
        self.assertEqual(left_tree.root.rank, 10)
        self.assertEqual(left_tree.root.left.rank, 5)
        self.assertEqual(left_tree.root.right.rank, 15)
        self.assertEqual(right_tree.root.rank, 20)
        self.assertEqual(right_tree.root.left.rank, 18)
        self.assertEqual(right_tree.root.right.rank, 25)

    def test_get_message_from_trees(self):
        """
        Test extracting the final message from two BSTs.
        """
        from day02_part2 import get_message_from_trees
        left_nodes = [(10, 'A'), (5, 'B'), (15, 'C'), (12, 'D')]
        right_nodes = [(20, 'X'), (25, 'Y'), (18, 'Z'), (22, 'Q')]
        left_tree = BinarySearchTree()
        for i, (rank, sym) in enumerate(left_nodes):
            left_tree.insert(rank, sym, f"L{i}")
        right_tree = BinarySearchTree()
        for i, (rank, sym) in enumerate(right_nodes):
            right_tree.insert(rank, sym, f"R{i}")
        msg = get_message_from_trees(left_tree, right_tree)
        self.assertEqual(set(msg), set(['B', 'C', 'Z', 'Y']))
        self.assertEqual(len(msg), 4)

    def test_problem_example(self):
        """
        Test the full process using the example from the problem statement (should output MGFLNK).
        """
        from day02_part2 import process_commands_incremental, get_message_from_trees
        import tempfile
        lines = [
            "ADD id=1 left=[10,A] right=[30,H]",
            "ADD id=2 left=[15,D] right=[25,I]",
            "ADD id=3 left=[12,F] right=[31,J]",
            "ADD id=4 left=[5,B] right=[27,L]",
            "ADD id=5 left=[3,C] right=[28,M]",
            "SWAP 1",
            "SWAP 5",
            "ADD id=6 left=[20,G] right=[32,K]",
            "ADD id=7 left=[4,E] right=[21,N]"
        ]
        with tempfile.NamedTemporaryFile(mode="w+", delete=False) as f:
            for line in lines:
                f.write(line + "\n")
            fname = f.name
        left_tree, right_tree = process_commands_incremental(fname)
        msg = get_message_from_trees(left_tree, right_tree)
        self.assertEqual(msg, "MGFLNK")

if __name__ == "__main__":
    unittest.main()
