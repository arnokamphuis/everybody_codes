---
issue_url: https://github.com/arnokamphuis/everybody_codes/issues/5
---
## Context (User Story)
You want to implement a solution for "The Tangled Trees Gambit" puzzle, Part II (SWAP Edition). The user is given a list of commands to add pairs of nodes to two separate binary trees (left and right). Each node has a unique rank and a symbol. SWAP commands can appear at any point and swap the rank and symbol of the nodes with the same ID between the two trees. After building both trees incrementally, the solution should find the level with the most nodes in each tree and concatenate the symbols at those levels (left tree first, then right) to form a final message.

## Objective & Acceptance Criteria
- **Goal:** Parse the input commands (including SWAPs), build the two binary trees incrementally, and output a string of capital letters formed by concatenating the symbols from the most populated level of each tree (left first, then right).
- **Acceptance Criteria:**
  - The output is a single string of capital letters.
  - The solution reads from the provided input file.
  - SWAP commands swap the rank and symbol of the nodes with the same ID between the two trees, affecting the structure of both trees for all subsequent operations.
  - The implementation is clear, testable, and follows the project’s conventions.

## High-Level Technical Outline
- Process the input file incrementally, building the trees as commands are read.
- For each ADD, insert the left and right node into their respective trees, tracking the ID.
- For each SWAP, swap the rank and symbol of the nodes with the same ID between the two trees.
- Traverse each tree to find the level with the most nodes.
- Collect and concatenate the symbols from those levels (left-to-right order).
- Output the result as a string.

## Task Breakdown

1. **Process Input and Build Trees Incrementally**  
   - [x] **Type:** backend  
   - **Outline:** Read and process the input file, handling both ADD and SWAP commands in order. Build the trees as you go, swapping nodes in both trees for SWAPs.  
   - **Dependencies:** None  
   - **Blockers:** None

2. **Implement Binary Search Tree Class with SWAP Support**  
   - [x] **Type:** backend  
   - **Outline:** Create a BST class that supports node insertion, level-order traversal, and swapping nodes by ID.  
   - **Dependencies:** None  
   - **Blockers:** None

3. **Find Most Populated Level and Collect Symbols**  
   - [x] **Type:** backend  
   - **Outline:** Traverse each tree to find the level with the most nodes and collect the symbols at that level.  
   - **Dependencies:** Task 2  
   - **Blockers:** None

4. **Output the Final Message**  
   - [x] **Type:** backend  
   - **Outline:** Concatenate the symbols from both trees and print the result.  
   - **Dependencies:** Task 3  
   - **Blockers:** None

5. **Write Unit Tests**  
   - [x] **Type:** backend  
   - **Outline:** Add tests to verify tree construction, SWAP logic, level detection, and output correctness.  
   - **Dependencies:** Tasks 1-4  
   - **Blockers:** None

6. **Update Documentation**  
   - [x] **Type:** documentation  
   - **Outline:** Add a Markdown file in `/docs` describing the puzzle, approach, and usage.  
   - **Dependencies:** Tasks 1-5  
   - **Blockers:** None

## Documentation Impact
- New Markdown documentation in `/docs` for Day 2, 2025, Part II (SWAP Edition).
- Update `README.md` if a list of puzzles/solutions is maintained.
