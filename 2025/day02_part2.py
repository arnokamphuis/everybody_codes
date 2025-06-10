"""
Day 2, 2025 - Part II: Tangled Trees Gambit (SWAP Edition)

This script parses the input file, processes ADD and SWAP commands, and prepares node pairs for tree construction.
"""
import os
import re

def parse_commands(filepath):
    """
    Parses the input file and returns two lists:
    - left_nodes: list of (rank, symbol) for the left tree
    - right_nodes: list of (rank, symbol) for the right tree
    after all SWAPs are processed, in the order of ADDs.
    SWAP exchanges the *entire* left and right node (rank and symbol) for the given ID.
    """
    node_map = {}
    add_order = []
    add_pattern = re.compile(r"ADD id=(\d+) left=\[(\d+),([A-Za-z!])\] right=\[(\d+),([A-Za-z!])\]")
    swap_pattern = re.compile(r"SWAP (\d+)")
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            m_add = add_pattern.match(line)
            m_swap = swap_pattern.match(line)
            if m_add:
                id_, l_rank, l_sym, r_rank, r_sym = m_add.groups()
                node_map[id_] = [(int(l_rank), l_sym), (int(r_rank), r_sym)]
                add_order.append(id_)
            elif m_swap:
                id_ = m_swap.group(1)
                if id_ in node_map:
                    # Swap the *entire* left and right node (rank and symbol)
                    node_map[id_][0], node_map[id_][1] = node_map[id_][1], node_map[id_][0]
    left_nodes = [node_map[id_][0] for id_ in add_order]
    right_nodes = [node_map[id_][1] for id_ in add_order]
    return left_nodes, right_nodes

def build_trees(left_nodes, right_nodes):
    """
    Builds two BSTs from the provided node lists.
    Returns (left_tree, right_tree).
    """
    left_tree = BinarySearchTree()
    right_tree = BinarySearchTree()
    for l_rank, l_sym in left_nodes:
        left_tree.insert(l_rank, l_sym)
    for r_rank, r_sym in right_nodes:
        right_tree.insert(r_rank, r_sym)
    return left_tree, right_tree

def process_commands_incremental(filepath):
    """
    Process commands incrementally, building the trees as you go and swapping nodes in the trees for SWAPs.
    Returns (left_tree, right_tree).
    """
    left_tree = BinarySearchTree()
    right_tree = BinarySearchTree()
    add_pattern = re.compile(r"ADD id=(\d+) left=\[(\d+),([A-Za-z!])\] right=\[(\d+),([A-Za-z!])\]")
    swap_pattern = re.compile(r"SWAP (\d+)" )
    with open(filepath, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("//"):
                continue
            m_add = add_pattern.match(line)
            m_swap = swap_pattern.match(line)
            if m_add:
                id_, l_rank, l_sym, r_rank, r_sym = m_add.groups()
                left_tree.insert(int(l_rank), l_sym, id_)
                right_tree.insert(int(r_rank), r_sym, id_)
            elif m_swap:
                id_ = m_swap.group(1)
                left_tree.swap_nodes_between_trees(right_tree, id_)
    return left_tree, right_tree

# --- Binary Search Tree Implementation for Tangled Trees Gambit (Part II) ---

class BSTNode:
    """
    Node for the Binary Search Tree (BST).
    Each node holds a rank (for placement) and a symbol (the letter to collect).
    """
    def __init__(self, rank, symbol, id_=None):
        self.rank = rank  # Integer used for BST placement
        self.symbol = symbol  # Capital letter or symbol
        self.left = None  # Left child
        self.right = None  # Right child
        self.id = id_  # Track the id for SWAPs

class BinarySearchTree:
    """
    Binary Search Tree supporting insertion and level-order traversal.
    """
    def __init__(self):
        self.root = None
        self.id_map = {}  # id -> node

    def insert(self, rank, symbol, id_):
        """
        Insert a node into the BST by rank.
        """
        if not self.root:
            self.root = BSTNode(rank, symbol, id_)
            self.id_map[id_] = self.root
            return
        curr = self.root
        while True:
            if rank < curr.rank:
                if curr.left:
                    curr = curr.left
                else:
                    curr.left = BSTNode(rank, symbol, id_)
                    self.id_map[id_] = curr.left
                    return
            else:
                if curr.right:
                    curr = curr.right
                else:
                    curr.right = BSTNode(rank, symbol, id_)
                    self.id_map[id_] = curr.right
                    return

    def swap_by_id(self, id1, id2):
        n1 = self.id_map.get(id1)
        n2 = self.id_map.get(id2)
        if n1 and n2:
            n1.rank, n2.rank = n2.rank, n1.rank
            n1.symbol, n2.symbol = n2.symbol, n1.symbol

    def swap_nodes_between_trees(self, other_tree, id_):
        n1 = self.id_map.get(id_)
        n2 = other_tree.id_map.get(id_)
        if n1 and n2:
            n1.rank, n2.rank = n2.rank, n1.rank
            n1.symbol, n2.symbol = n2.symbol, n1.symbol

    def level_order(self):
        """
        Returns a list of lists: each sublist contains (rank, symbol) tuples for a level.
        Uses a queue for breadth-first traversal.
        """
        from collections import deque
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
        """
        Returns a list of symbols from the most populated level (first such level if tie).
        """
        levels = self.level_order()
        if not levels:
            return []
        max_len = max(len(lvl) for lvl in levels)
        for lvl in levels:
            if len(lvl) == max_len:
                return [sym for _, sym in lvl]
        return []

def get_message_from_trees(left_tree, right_tree):
    """
    Returns the concatenated message from the most populated level of each tree (left first, then right).
    """
    left_syms = left_tree.most_populated_level_symbols()
    right_syms = right_tree.most_populated_level_symbols()
    return ''.join(left_syms + right_syms)

def main():
    """
    Main entry point: parses input, builds trees, and prints the final message.
    """
    import os
    INPUT_FILE = os.path.join(os.path.dirname(__file__), "input", "everybody_codes_e1_q02_p2.txt")
    left_tree, right_tree = process_commands_incremental(INPUT_FILE)
    message = get_message_from_trees(left_tree, right_tree)
    print(message)

if __name__ == "__main__":
    main()
