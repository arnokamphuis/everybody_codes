from collections import defaultdict
from copy import deepcopy
from filecmp import cmp
import functools
import sys
from time import perf_counter, sleep
from grapheme import length
from sympy import ceiling, floor, prod


# Day identifier used to locate input files for this puzzle/day
day = 11


# The script expects two CLI args: the part number and which input set to use
# Example usage: `python day11.py 1 test`  or `python day11.py 2 real`
if len(sys.argv) != 3:
    print("invalid command")
    exit()

# `part` chooses which puzzle/algorithm to run (1, 2 or 3 for this file)
part = int(sys.argv[1])
# `sort` chooses which input file variant to use (usually 'test' or 'real')
sort = sys.argv[2]


def run(part, sort):
    """Run the chosen part of the puzzle using the selected input file.

    The input files are expected to live under `input/day{day:02d}` and be
    named like `p{part}-test.txt` or `p{part}-real.txt`.

    This file implements logic to "equalize" a list of integer columns by
    repeatedly transferring units between adjacent columns until a steady
    pattern is reached. The functions below compute different measures:
      - `equalize` returns a list of weighted checksums observed during
        iterative balancing rounds.
      - `steps_in_phase` analyzes a single balancing phase and estimates the
        number of steps required to move columns to a phase-1 target.
      - `determine_steps` combines phase analysis to compute a total step
        count for complete equalization.

    The rest of the function orchestrates reading input, invoking these
    helpers, and printing timed results for three possible `part` values.
    """

    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    # Read and strip all lines from the input file
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    # Start a timer (used purely for reporting microseconds later)
    start = perf_counter()
    result = None

    # Parse the input lines into integers representing column heights
    columns = list(map(int, data))


    def equalize(columns):
        """Perform iterative balancing of adjacent columns.

        Approach:
        - `checksums` records a weighted sum after each completed round. The
          weighted sum uses indices starting from 1, i.e. sum(idx * value).
        - The algorithm runs in two "phases": first `phase = 1` where the
          goal is to move mass right-to-left (decrement left, increment
          right) when the left column is greater than the right; then
          `phase = -1` reverses the direction.
        - During a single round we iterate over adjacent pairs and, when a
          pair is out of order for the current phase, transfer a single unit
          (plus or minus `phase`) from one column to the other.
        - If at least one transfer occurs in the round we append the new
          weighted checksum and continue. If no transfers occur we switch
          phases once; if still no transfers the process terminates.

        Returns:
        - `checksums`: a list of weighted sums recorded after each performed round.
        """

        # Initialize checksums with the initial weighted checksum
        checksums = [sum([idx * v for idx, v in enumerate(columns, start=1)])]
        round = 0
        phase = 1

        # Repeat until both phases perform no transfers
        while True:
            performed = False

            # Walk adjacent pairs and perform one-unit transfers when needed
            for step in range(1, len(columns)):
                # If current pair satisfies the order for this phase, skip
                if (phase == 1 and columns[step - 1] <= columns[step]) or (
                    phase == -1 and columns[step - 1] >= columns[step]
                ):
                    continue
                else:
                    # Move one unit according to the phase direction:
                    # when phase == 1: decrement left, increment right
                    # when phase == -1: increment left, decrement right
                    columns[step - 1], columns[step] = (
                        columns[step - 1] - phase,
                        columns[step] + phase,
                    )
                    performed = True

            if performed:
                # A round of transfers happened; record its checksum
                round += 1
                checksums.append(sum([idx * v for idx, v in enumerate(columns, start=1)]))
            else:
                # No transfers happened in this phase; flip from phase 1 to -1
                if phase == 1:
                    phase = -1
                else:
                    # Phase -1 also had no transfers -> balancing complete
                    break

        return checksums


    def steps_in_phase(columns):
        """Analyze the first balancing phase and estimate steps required.

        This function partitions the `columns` array into consecutive ranges
        where each range starts at index `idx` and extends while the next
        column is strictly less than the starting column. For each such
        segment it computes a target distribution (`phase1_cols`) representing
        how values would be split in the first phase and computes the
        number of unit-transfers `delta` required for that segment.

        Return value:
          - `steps`: maximum delta across segments (the dominant cost in phase 1)
          - `phase1_cols`: the per-index values after completing phase 1 targets
        """

        idx = 0
        ndx = 1
        delta = 0
        steps = 0
        # Work on a copy to avoid mutating the caller's list
        phase1_cols = deepcopy(columns)

        # Partition into runs where columns[ndx] < columns[idx]
        while True:
            delta = 0
            value = columns[idx]

            # Extend `ndx` while next columns are strictly smaller than start
            while ndx < len(columns) and columns[ndx] < columns[idx]:
                value += columns[ndx]
                ndx += 1

            # `value` now holds the sum of the segment [idx, ndx)
            # Compute how many cells in the segment will receive the smaller
            # integer via division remainder logic.
            cdx = value % (ndx - idx)
            avg = value // (ndx - idx)

            # Fill `phase1_cols` for the segment: the first `cdx` cells get `avg`,
            # the rest get `avg+1` so the total sums to `value`.
            for ii in range(idx, ndx):
                if ii < cdx + idx:
                    phase1_cols[ii] = avg
                else:
                    phase1_cols[ii] = avg + 1

                # Count how many unit transfers this index needs to reach avg
                if columns[ii] <= avg:
                    # If original value <= avg, it needs (avg - original) units.
                    # For indices after the `cdx` boundary add an extra unit.
                    d = avg - columns[ii] + (1 if ii > cdx + idx else 0)
                    delta += d

            # The number of steps required for this segment is `delta`; keep
            # the maximum across segments since segments operate in parallel.
            steps = max(steps, delta)

            # Move to the next segment
            idx = ndx
            ndx = idx + 1
            if idx >= len(columns):
                break

        return steps, phase1_cols


    def determine_steps(columns):
        """Combine phase analysis to compute total step count for equalization.

        `determine_steps` first computes the dominant cost (`steps`) needed in
        the first phase (via `steps_in_phase`). It then computes a global
        average `avg` of the `phase1_cols` and counts how many unit moves are
        still needed to bring all values up to the average. The result is the
        sum of phase1 steps and this balancing delta.
        """

        steps, phase1_cols = steps_in_phase(columns)

        delta = 0
        # Global average after phase 1 rounding-down (floor division)
        avg = sum(phase1_cols) // len(phase1_cols)
        for ii in range(len(phase1_cols)):
            if phase1_cols[ii] >= avg:
                # Count surplus above the average; these will be redistributed
                delta += phase1_cols[ii] - avg
        return steps + delta


    # --- Part 1 ---
    if part == 1:
        # The original code returns the 11th recorded checksum (index 10)
        result = equalize(columns)[10]
    # --- Part 2 ---
    elif part == 2:
        # Several alternative approaches were present in the original file.
        # Here the chosen behavior returns the number of rounds performed
        # (length of checksums list minus the initial entry).
        result = len(equalize(columns)) - 1
    # --- Part 3 ---
    elif part == 3:
        # Use the analytical step-determination routine to compute steps
        result = determine_steps(columns)

    # Stop timing and print result with microsecond precision (rounded up)
    end = perf_counter()

    # Print the result and elapsed time in microseconds (rounded up).
    print(
        f"Part {part}: ({int(ceiling((end - start) * 1000000)):>12} microseconds): \t{result}"
    )


if part == 0:
    # When `part` is 0 run all parts in sequence
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)