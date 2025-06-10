# Day 1, 2025 Part II: Enigmatus Modular Puzzle Solution (Truncated)

## Overview
This module solves Part II of the "eni" modular arithmetic puzzle from the Echoes of Enigmatus story.

- Implements the truncated `eni` function (last 5 remainders) as described in the story.
- Reads parameter sets from an input file.
- Computes the sum for each set: `eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)` using the truncated function.
- Finds and prints the highest result.

## How the Solution Works

1. **eni_truncated(N, EXP, MOD, k=5):**
   - Multiplies `N` by itself `EXP` times, each time taking the remainder modulo `MOD`.
   - Each remainder is prepended to a list.
   - Only the last `k` remainders are kept (default 5).
   - The list is joined into a single integer (as a string, then converted to int).
2. **Input Parsing:**
   - Each line in the input file is parsed for variables A, B, C, X, Y, Z, M.
3. **Computation:**
   - For each line, computes the sum: `eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)` using the truncated function.
   - Tracks the highest sum found.
4. **Output:**
   - Prints the highest result.

## Usage

1. Place your input file in the correct directory (see the script for the path).
2. Run the script:
   ```bash
   python 2025/day01_part2.py
   ```
3. The script will print the highest result.

## Unit Tests
- Run the tests with:
  ```bash
  python -m unittest 2025/test_day01_part2.py
  ```

## Further Reading
- [Python's Modulo Operator](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)
- [Unit Testing in Python](https://docs.python.org/3/library/unittest.html)
