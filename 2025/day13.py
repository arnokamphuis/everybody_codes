from collections import deque
import sys
from time import perf_counter
from sympy import ceiling


# Day identifier used to locate input files for this puzzle/day
day = 13


# The script expects exactly two CLI args: the part number and which input set
# to use. Typical usage examples:
#   python day13.py 1 test    # run part 1 on the 'test' input
#   python day13.py 2 real    # run part 2 on the 'real' input
if len(sys.argv) != 3:
    print("invalid command")
    exit()

# `part` chooses which puzzle/algorithm to run (1, 2 or 3 for this file)
part = int(sys.argv[1])
# `sort` chooses which input file variant to use (usually 'test' or 'real')
sort = sys.argv[2]


def run(part, sort):
    """Run the selected part using the given input variant.

    The input file is expected at `input/day{day:02d}/p{part}-{sort}.txt`.
    The file lines are interpreted as tokens which may be either the integer
    literal `1` or a hyphen-separated range like `10-20`.

    High-level behavior implemented in this file:
      - Parse input tokens into an ordered list `numbers`.
      - Re-arrange tokens into two lists (`left` and `right`) using a
        simple alternating split, then recombine them so the center pivot is `1`.
      - `find_number` maps a large turn-count into the actual number that would
        appear at that position if the ranges in `numbers` were expanded.

    Note: This function focuses on explaining the algorithm; it intentionally
    does not change the original program's logic.
    """

    # Build the path to the input file and read stripped lines
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    # The puzzle input is treated as a sequence of tokens (strings)
    numbers = [line for line in data]

    # The original code splits the list of tokens into two lists (`left` and
    # `right`) by alternating tokens between them. This appears to perform a
    # positional rebalancing so that later the pivot token `1` can be centered.
    left = []
    right = [1]

    # `cw` acts as a simple toggle alternating assignment between right/left
    cw = True
    for n in numbers:
        if cw:
            right.append(n)
            cw = False
        else:
            left.append(n)
            cw = True

    # After the loop `left` contains every second token (starting from the
    # second), `right` contains the others prefixed by the literal `1`.
    # The code then reverses `left`, concatenates it to `right` and rotates the
    # result so that the first occurrence of `1` becomes the front. This yields
    # a circular arrangement with `1` as the pivot.
    numbers = left[::-1] + right
    idx = numbers.index(1)
    numbers = numbers[idx:] + numbers[:idx]

    # Start a timer to measure elapsed time for this run (reported in microseconds)
    start = perf_counter()
    result = None


    def find_number(nums, turns):
        """Map a large `turns` index into a concrete integer by interpreting
        `nums` as compressed ranges.

        `nums` is a list of tokens where each token is either the integer 1
        (treated specially as the singleton range [1,1]) or a string like
        'A-B' representing the inclusive integer range [A, B].

        Algorithm outline:
        1. Convert tokens into explicit [start, end] integer pairs.
        2. Compute the length (count of integers) of each range and the
           total length.
        3. Reduce `turns` modulo the total length to find the offset within
           the repeated expansion of the circular sequence.
        4. Walk the range lengths until locating the range containing the
           desired offset. Depending on whether that textual range originally
           belonged to the `left` list (created earlier), compute the value
           using either descending or ascending mapping.

        This logic effectively simulates reading the circular, expanded
        sequence of integers and reporting the value at position `turns`.
        """

        # Convert token list to explicit numeric ranges: [start, end]
        numbers = [list(map(int, n.split('-'))) if n != 1 else [1, 1] for n in nums]

        # Length of each numeric block (inclusive)
        lengths = [b - a + 1 for a, b in numbers]

        # Total number of integers represented by all blocks
        length = sum(lengths)

        # Reduce target index modulo the total cycle length
        rest = (turns % length)

        last_range = []
        # Pop ranges from the front until the target offset falls within one
        while True:
            n = lengths.pop(0)
            last_range = numbers.pop(0)
            if rest >= n:
                rest -= n
            else:
                break

        # Determine if the textual representation of the selected range was in
        # the `left` list. The original code uses this to decide whether the
        # mapping within the range is reversed (descending) or normal (ascending).
        if f"{last_range[0]}-{last_range[1]}" in left:
            # If the range belonged to `left`, count from the end downwards
            result = last_range[-1] - rest
        else:
            # Otherwise count from the start upwards
            result = last_range[0] + rest

        return result


    # --- Part 1: return the token at (2025 mod N) ---
    if part == 1:
        result = numbers[2025 % len(numbers)]

    # --- Part 2: map a very large turn count into the actual integer ---
    elif part == 2:
        result = find_number(numbers, 20252025)

    # --- Part 3: same mapping but with an even larger turn count ---
    elif part == 3:
        result = find_number(numbers, 202520252025)

    # Stop timing and print result with microsecond precision (rounded up)
    end = perf_counter()
    print(f"Part {part}: ({int(ceiling((end - start) * 1000000)):>12} microseconds): \t{result}")


if part == 0:
    # Convenience mode: run all parts in sequence
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)