---
description: Refactor code for improved maintainability in a step-by-step manner.
---

# Code Refactoring for Maintainability - Agent Mode

**Goal:** Refactor the selected code (or the codebase if no selection) to significantly improve its maintainability, readability, testability, and adherence to best practices. This should be a thorough, step-by-step process, with clear documentation of each change.

**Agent Instructions:**

1.  **Understand the Current State:**
    * First, analyze the provided code context (files, selection, current working directory).
    * Identify areas that specifically hinder maintainability. Think about:
        * Code duplication (DRY principle violations)
        * Long functions/methods
        * Complex conditional logic (high cyclomatic complexity)
        * Poor naming conventions
        * Lack of clear separation of concerns
        * Tight coupling between modules/components
        * Missing or unclear comments/documentation
        * Inefficient algorithms or data structures (if they impact maintainability and readability)
    * **Crucially, use the Memory MCP to store an initial assessment and a "before" snapshot of the relevant code/files.**

2.  **Propose a Refactoring Plan (Step-by-Step):**
    * Based on the analysis, generate a detailed, ordered list of refactoring steps.
    * Each step should be small, atomic, and explain its specific purpose for maintainability.
    * For each step, specify:
        * **What** needs to be refactored (e.g., "Extract function `calculateTotalPrice` from `processOrder`").
        * **Why** this refactoring improves maintainability (e.g., "Reduces function length, improves readability, and makes `calculateTotalPrice` reusable and testable in isolation.").
        * **Which files** are likely to be affected.
    * **Leverage the SequentialThinking MCP to ensure a logical flow of refactoring operations, addressing dependencies between steps.**

3.  **Execute Refactoring Steps Iteratively:**
    * For each step in the generated plan:
        * Apply the code changes.
        * **After each significant change, use the Memory MCP to record the "after" state of the affected files and a summary of the change.** This is essential for tracking progress and for potential rollback.
        * If unit tests exist, suggest running them to verify that the changes haven't introduced regressions. If tests don't exist, suggest creating basic tests for the refactored logic.
        * Address any new issues (linting errors, compilation errors) introduced by the change.
        * Provide a brief update on the progress of the current step.

4.  **Review and Verify:**
    * Once all planned refactoring steps are completed, perform a final review of the entire refactored codebase.
    * Identify any remaining areas for improvement based on the initial goal.
    * Summarize all the changes made and how they contribute to improved maintainability.
    * Suggest creating a Git commit for the refactoring. **(Potentially leverage GitHub MCP for this).**

**Constraints/Guidelines:**

* **Maintain functionality:** The refactored code *must* retain its original functionality. Prioritize correctness over speed.
* **No new features:** Do not add any new features during this refactoring process. Focus solely on improving existing code.
* **Preserve external APIs:** Do not change public API signatures unless absolutely necessary for maintainability and with explicit justification.
* **Clear and concise commits (if committing):** Each logical refactoring step should ideally correspond to a clear, descriptive commit message.
* **Follow existing coding style/conventions:** Adapt to the existing code style, naming conventions, and project structure.
* **Prioritize readability:** Aim for code that is easy for other developers (and your future self) to understand.
* **Be explicit with comments:** Add comments where the purpose of a change or complex logic might not be immediately obvious.
* **Justify major architectural changes:** If a proposed refactoring involves a significant architectural shift, explain the rationale clearly before proceeding.

---