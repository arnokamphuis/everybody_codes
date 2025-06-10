# Tangled Trees Gambit: Day 2, 2025 Part I

---

## Puzzle Description

Given a list of commands to add pairs of nodes to two separate binary trees (left and right), each node has a unique rank and a symbol. After building both trees, find the level with the most nodes in each tree and concatenate the symbols at those levels (left tree first, then right) to form a final message.

## Approach

1. **Parse Input:** Read the input file and extract node pairs for both trees.
2. **Build Trees:** Insert nodes into two independent binary search trees (BSTs) using the rank for placement.
3. **Find Most Populated Level:** Traverse each tree to find the level with the most nodes and collect the symbols at that level.
4. **Output:** Concatenate the symbols from both trees and print the result as a string of capital letters.

## Usage

```bash
python 2025/day02_part1.py
```

The script will read the input from `2025/input/everybody_codes_e1_q02_p1.txt` and print the final message.

## Testing

Run all tests with:

```bash
python -m unittest 2025/test_day02_part1.py
```

## Further Reading

- [Binary Search Tree (BST) – GeeksforGeeks](https://www.geeksforgeeks.org/binary-search-tree-data-structure/)
- [Level Order Traversal – GeeksforGeeks](https://www.geeksforgeeks.org/level-order-tree-traversal/)
