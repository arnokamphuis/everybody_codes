# Tangled Trees Gambit: Day 2, 2025 Part II (SWAP Edition)

## Puzzle Overview
In this challenge, you are given a list of commands to build two binary search trees (BSTs):
- `ADD` commands add a pair of nodes (left and right) with a unique ID, rank, and symbol.
- `SWAP` commands swap the left and right nodes (rank and symbol) for a given ID **in both trees**.

After all commands are processed, the trees are built incrementally as commands are read. For each `SWAP`, the nodes with the same ID in both trees exchange their rank and symbol. The answer is formed by finding the most populated level in each tree and concatenating the symbols at those levels (left tree first, then right).

## Approach
1. **Process Commands Incrementally:**
   - For each `ADD`, insert the left and right node into their respective trees, tracking the ID.
   - For each `SWAP`, swap the rank and symbol of the nodes with the given ID between the two trees.
2. **Build Trees:**
   - The trees are built as you process the commands; no post-processing is needed.
3. **Find Most Populated Level:**
   - Traverse each tree level by level (breadth-first).
   - Find the level with the most nodes and collect the symbols at that level (left-to-right order).
4. **Output:**
   - Concatenate the symbols from the left tree's most populated level, then the right tree's, and print the result.

## Example
Suppose the input is:
```
ADD id=1 left=[10,A] right=[30,H]
ADD id=2 left=[15,D] right=[25,I]
ADD id=3 left=[12,F] right=[31,J]
ADD id=4 left=[5,B] right=[27,L]
ADD id=5 left=[3,C] right=[28,M]
SWAP 1
SWAP 5
ADD id=6 left=[20,G] right=[32,K]
ADD id=7 left=[4,E] right=[21,N]
```
After processing, the most populated level in the left tree is `MGF` and in the right tree is `LNK`. The final answer is `MGFLNK`.

## How to Run
```bash
python 2025/day02_part2.py
```

## Testing
Run all tests with:
```bash
python -m unittest 2025/test_day02_part2.py
```

## Further Reading
- [Binary Search Tree (BST) – GeeksforGeeks](https://www.geeksforgeeks.org/binary-search-tree-data-structure/)
- [Level Order Traversal – GeeksforGeeks](https://www.geeksforgeeks.org/level-order-tree-traversal/)
