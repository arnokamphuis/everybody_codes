---
issue_url: https://github.com/arnokamphuis/everybody_codes/issues/4
---
## Context (User Story)
You want to implement a solution for "The Tangled Trees Gambit" puzzle. The user is given a list of commands to add pairs of nodes to two separate binary trees (left and right). Each node has a unique rank and a symbol. After building both trees, the solution should find the level with the most nodes in each tree and concatenate the symbols at those levels (left tree first, then right) to form a final message.

## Objective & Acceptance Criteria
- **Goal:** Parse the input commands, build the two binary trees, and output a string of capital letters formed by concatenating the symbols from the most populated level of each tree (left first, then right).
- **Acceptance Criteria:**
  - The output is a single string of capital letters.
  - The solution reads from the provided input file.
  - The implementation is clear, testable, and follows the project’s conventions.

## High-Level Technical Outline
- Parse the input file to extract node pairs.
- Build two independent binary search trees (BSTs) using the rank for placement.
- Traverse each tree to find the level with the most nodes.
- Collect and concatenate the symbols from those levels.
- Output the result as a string.

## Task Breakdown

1. **Parse Input File**  
   - [x] **Type:** backend  
   - **Outline:** Read and parse the input file to extract node pairs for both trees.  
   - **Dependencies:** None  
   - **Blockers:** None

2. **Implement Binary Search Tree Class**  
   - [x] **Type:** backend  
   - **Outline:** Create a BST class that supports node insertion and level-order traversal.  
   - **Dependencies:** None  
   - **Blockers:** None

3. **Build Trees from Input**  
   - [x] **Type:** backend  
   - **Outline:** Use the parsed input to build the left and right trees.  
   - **Dependencies:** Tasks 1, 2  
   - **Blockers:** None

4. **Find Most Populated Level and Collect Symbols**  
   - [x] **Type:** backend  
   - **Outline:** Traverse each tree to find the level with the most nodes and collect the symbols at that level.  
   - **Dependencies:** Task 3  
   - **Blockers:** None

5. **Output the Final Message**  
   - [x] **Type:** backend  
   - **Outline:** Concatenate the symbols from both trees and print the result.  
   - **Dependencies:** Task 4  
   - **Blockers:** None

6. **Write Unit Tests**  
   - [x] **Type:** backend  
   - **Outline:** Add tests to verify tree construction, level detection, and output correctness.  
   - **Dependencies:** Tasks 1-5  
   - **Blockers:** None

7. **Update Documentation**  
   - [x] **Type:** documentation  
   - **Outline:** Add a Markdown file in `/docs` describing the puzzle, approach, and usage.  
   - **Dependencies:** Tasks 1-5  
   - **Blockers:** None

## Documentation Impact
- New Markdown documentation in `/docs` for Day 2, 2025, Part I.
- Update `README.md` if a list of puzzles/solutions is maintained.
