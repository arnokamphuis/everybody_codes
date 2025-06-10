---
issue_url: https://github.com/arnokamphuis/everybody_codes/issues/2
---
## Context

In Part II of Day 1, 2025, the story introduces a practical limitation to the original `eni` function: when input values are very large, the resulting numbers become unwieldy. To address this, only the last 5 remainders from the iterative process are used to form the final number. The user must process a new list of parameter sets, apply this truncated `eni` function, and determine the highest result as before.

## Objective & Acceptance Criteria

**Objective:**  
Implement a Python module that reads parameter sets from an input file, applies the truncated `eni` function (using only the last 5 remainders), computes the required sums, and outputs the highest result.

**Acceptance Criteria:**
- The script implements the truncated `eni(N, EXP, MOD)` function as described (last 5 remainders only).
- It reads all parameter sets from the specified input file.
- For each set, it computes: `eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)` using the truncated function.
- It outputs the highest sum found.
- The code is well-documented, with inline explanations and a Markdown file in `/docs`.
- Unit tests are provided for the truncated `eni` function and the overall computation.
- The `README.md` is updated to reference this feature.

## High-Level Technical Outline

- **Input Parsing:** Read and parse each line of the input file for variables A, B, C, X, Y, Z, M.
- **Truncated eni Function:** Implement the custom modular arithmetic function, but only use the last 5 remainders to form the result.
- **Computation:** For each parameter set, compute the sum and track the maximum.
- **Testing:** Provide unit tests for the truncated `eni` function and the overall computation.
- **Documentation:** Update `/docs` and `README.md` with clear instructions and explanations.

## Task Breakdown

1. **Implement the truncated `eni` function**  
   - Type: backend  
   - Dependencies: None  
   - Outline: Write a function that multiplies a number by itself repeatedly, taking the modulus each time, and builds a number from the last 5 remainders.

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
   - Outline: Create tests for the truncated `eni` function and the overall computation using sample data.

5. **Document the solution**  
   - Type: documentation  
   - Dependencies: Tasks 1–4  
   - Outline: Write clear documentation in `/docs` and update `README.md`.

## Documentation Impact

- New documentation file: `/docs/day01_25_part2.md`
- Update to `README.md` with a section for this feature
- (Optional) Changelog entry if you maintain a `CHANGELOG.md`
