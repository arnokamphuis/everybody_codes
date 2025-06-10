---
issue_url: https://github.com/arnokamphuis/everybody_codes/issues/3
---
## Context

In Part III of Day 1, 2025, the story introduces a new variant of the `eni` function: instead of forming a number from the remainders, the function now sums all remainders obtained throughout the process. The user must process a new list of parameter sets, apply this sum-of-remainders `eni` function, and determine the highest result as before.

## Objective & Acceptance Criteria

**Objective:**  
Implement a Python module that reads parameter sets from an input file, applies the sum-of-remainders `eni` function, computes the required sums, and outputs the highest result.

**Acceptance Criteria:**
- The script implements the sum-of-remainders `eni(N, EXP, MOD)` function as described (sum all remainders along the way).
- It reads all parameter sets from the specified input file.
- For each set, it computes: `eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)` using the sum-of-remainders function.
- It outputs the highest sum found.
- The code is well-documented, with inline explanations and a Markdown file in `/docs`.
- Unit tests are provided for the sum-of-remainders `eni` function and the overall computation.
- The `README.md` is updated to reference this feature.

## High-Level Technical Outline

- **Input Parsing:** Read and parse each line of the input file for variables A, B, C, X, Y, Z, M.
- **Sum-of-Remainders eni Function:** Implement the custom modular arithmetic function, summing all remainders to form the result.
- **Computation:** For each parameter set, compute the sum and track the maximum.
- **Testing:** Provide unit tests for the sum-of-remainders `eni` function and the overall computation.
- **Documentation:** Update `/docs` and `README.md` with clear instructions and explanations.

## Task Breakdown

1. **Implement the sum-of-remainders `eni` function**  
   - Type: backend  
   - Dependencies: None  
   - Outline: Write a function that multiplies a number by itself repeatedly, taking the modulus each time, and sums all remainders.

2. **Parse the input file**  
   - Type: backend  
   - Dependencies: None  
   - Outline: Read each line, extract variables, and prepare them for computation.

3. **Compute sums and track the maximum**  
   - Type: backend  
   - Dependencies: Tasks 1, 2  
   - Outline: For each parameter set, compute the sum and update the maximum if needed.

4. **Write unit tests**  
   - Type: enabling  
   - Dependencies: Tasks 1, 3  
   - Outline: Create tests for the sum-of-remainders `eni` function and the overall computation using sample data.

5. **Document the solution**  
   - Type: documentation  
   - Dependencies: Tasks 1–4  
   - Outline: Write clear documentation in `/docs` and update `README.md`.

## Documentation Impact

- New documentation file: `/docs/day01_25_part3.md`
- Update to `README.md` with a section for this feature
- (Optional) Changelog entry if you maintain a `CHANGELOG.md`

## Progress Update (2025-06-10)

- [x] Implemented `eni_sum_remainders` with efficient cycle detection.
- [x] Added input parsing and computation logic to `2025/day01_part3.py`.
- [x] Created comprehensive unit tests in `2025/test_day01_part3.py`.
- [x] Wrote documentation in `/docs/day01_25_part3.md`.
- [x] Updated `README.md` to reference Part III.
- [x] All code, tests, and documentation are complete and up to date.

**Part III is now fully implemented and documented.**
