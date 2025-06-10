---
issue_url: https://github.com/arnokamphuis/everybody_codes/issues/1
---
## Context

A reader of the "Echoes of Enigmatus" story encounters a mathematical puzzle involving a custom function, `eni`, which manipulates numbers using modular arithmetic in a unique way. The user must process a list of parameter sets, compute a sum for each, and determine the highest result. This feature will automate the solution, provide clear documentation, and include unit tests for learning and reproducibility.

## Objective & Acceptance Criteria

**Objective:**  
Implement a Python module that reads parameter sets from an input file, applies the `eni` function to each, computes the required sums, and outputs the highest result.

**Acceptance Criteria:**
- The script implements the `eni(N, EXP, MOD)` function as described in the story.
- It reads all parameter sets from the specified input file.
- For each set, it computes: `eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)`.
- It outputs the highest sum found.
- The code is well-documented, with inline explanations and a Markdown file in `/docs`.
- Unit tests are provided for the `eni` function and the overall computation.
- The `README.md` is updated to reference this feature.

## High-Level Technical Outline

- **Input Parsing:** Read and parse each line of the input file for variables A, B, C, X, Y, Z, M.
- **eni Function:** Implement the custom modular arithmetic function as described.
- **Computation:** For each parameter set, compute the sum and track the maximum.
- **Testing:** Provide unit tests for the `eni` function and the overall computation.
- **Documentation:** Update `/docs` and `README.md` with clear instructions and explanations.

## Task Breakdown

1. **Implement the `eni` function**  
   - Type: backend  
   - Dependencies: None  
   - Outline: Write a function that multiplies a number by itself repeatedly, taking the modulus each time, and builds a number from the sequence of remainders.

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
   - Outline: Create tests for the `eni` function and the overall computation using sample data.

5. **Document the solution**  
   - Type: documentation  
   - Dependencies: Tasks 1–4  
   - Outline: Write clear documentation in `/docs` and update `README.md`.

## Documentation Impact

- New documentation file: `/docs/day01_25.md`
- Update to `README.md` with a section for this feature
- (Optional) Changelog entry if you maintain a `CHANGELOG.md`
