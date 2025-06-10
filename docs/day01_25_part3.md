# Day 1, 2025 Part III: Enigmatus Modular Puzzle Solution (Sum of Remainders)

## Overview
This module solves Part III of the "eni" modular arithmetic puzzle from the Echoes of Enigmatus story.

- Implements the sum-of-remainders `eni` function as described in the story.
- Reads parameter sets from an input file.
- Computes the sum for each set: `eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)` using the sum-of-remainders function.
- Finds and prints the highest result.

## How the Solution Works

1. **eni_sum_remainders(N, EXP, MOD):**
   - Multiplies `N` by itself `EXP` times, each time taking the remainder modulo `MOD`.
   - Sums all remainders encountered in the sequence.
   - Uses cycle detection for efficiency with large exponents.
2. **Input Parsing:**
   - Each line in the input file is parsed for variables A, B, C, X, Y, Z, M.
3. **Computation:**
   - For each line, computes the sum: `eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)` using the sum-of-remainders function.
   - Tracks the highest sum found.
4. **Output:**
   - Prints the highest result.

## Usage

1. Place your input file in the correct directory (see the script for the path).
2. Run the script:
   ```bash
   python 2025/day01_part3.py
   ```
3. The script will print the highest result.

## Unit Tests
- Run the tests with:
  ```bash
  python -m unittest 2025/test_day01_part3.py
  ```

## Further Reading
- [Python's Modulo Operator](https://docs.python.org/3/reference/expressions.html#binary-arithmetic-operations)
- [Unit Testing in Python](https://docs.python.org/3/library/unittest.html)
- [Cycle Detection Algorithms](https://en.wikipedia.org/wiki/Cycle_detection)
