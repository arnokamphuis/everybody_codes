"""
Day 2, 2025 - Part I: Tangled Trees Gambit

This script parses the input file, builds two binary search trees (BSTs), and outputs the concatenated symbols from the most populated level of each tree.
"""
import os
import re
from collections import deque, defaultdict

INPUT_FILE = os.path.join(os.path.dirname(__file__), "input", "everybody_codes_e1_q02_p1.txt")

def parse_input(filepath):
    """
    Parses the input file and returns two lists of (rank, symbol) tuples for left and right trees.
    """
    left_nodes = []
    right_nodes = []
    pattern = re.compile(r"ADD id=\d+ left=\[(\d+),([A-Za-z!])\] right=\[(\d+),([A-Za-z!])\]")
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):  # skip comments or empty lines
                continue
            m = pattern.match(line)
            if m:
                l_rank, l_sym, r_rank, r_sym = m.groups()
                left_nodes.append((int(l_rank), l_sym))
                right_nodes.append((int(r_rank), r_sym))
    return left_nodes, right_nodes

class BSTNode:
    def __init__(self, rank, symbol):
        self.rank = rank
        self.symbol = symbol
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, rank, symbol):
        if not self.root:
            self.root = BSTNode(rank, symbol)
            return
        curr = self.root
        while True:
            if rank < curr.rank:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = BSTNode(rank, symbol)
                    return
            else:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = BSTNode(rank, symbol)
                    return

    def level_order(self):
        """
        Returns a list of lists: each sublist contains (rank, symbol) tuples for a level.
        """
        if not self.root:
            return []
        result = []
        queue = deque([(self.root, 0)])
        while queue:
            node, level = queue.popleft()
            if len(result) <= level:
                result.append([])
            result[level].append((node.rank, node.symbol))
            if node.left:
                queue.append((node.left, level+1))
            if node.right:
                queue.append((node.right, level+1))
        return result

    def most_populated_level_symbols(self):
        levels = self.level_order()
        if not levels:
            return []
        max_len = max(len(lvl) for lvl in levels)
        for lvl in levels:
            if len(lvl) == max_len:
                return [sym for _, sym in lvl]
        return []

def build_trees(left_nodes, right_nodes):
    """
    Builds two BSTs from the provided node lists.
    Returns (left_tree, right_tree).
    """
    left_tree = BinarySearchTree()
    right_tree = BinarySearchTree()
    for (l_rank, l_sym), (r_rank, r_sym) in zip(left_nodes, right_nodes):
        left_tree.insert(l_rank, l_sym)
        right_tree.insert(r_rank, r_sym)
    return left_tree, right_tree

def get_message_from_trees(left_tree, right_tree):
    """
    Returns the concatenated message from the most populated level of each tree (left first, then right).
    """
    left_syms = left_tree.most_populated_level_symbols()
    right_syms = right_tree.most_populated_level_symbols()
    return ''.join(left_syms + right_syms)

def main():
    left_nodes, right_nodes = parse_input(INPUT_FILE)
    left_tree, right_tree = build_trees(left_nodes, right_nodes)
    message = get_message_from_trees(left_tree, right_tree)
    print(message)

if __name__ == "__main__":
    main()
