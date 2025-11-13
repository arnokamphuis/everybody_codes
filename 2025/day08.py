from collections import defaultdict
from copy import deepcopy
import sys
from time import perf_counter
from sympy import ceiling, floor, prod
from functools import cmp_to_key

# Day identifier used to locate input files for this puzzle/day
day = 8

# The script expects two CLI args: the part number and which input set to use
# Example usage: `python day08.py 1 test`  or `python day08.py 2 real`
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
    """
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    # Read and strip all lines from the input file
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    # Start a timer (used purely for reporting microseconds later)
    start = perf_counter()
    result = None

    # --- Part 1 ---
    # Count the number of cords that form a specific diagonal relation.
    # The puzzle defines a number of nails around a circle; for small test
    # inputs we use 8 nails, for real inputs 32.
    if part == 1:
        if sort == 'test':
            nails = 8
        else:
            nails = 32
        # A cord is considered 'diagonal' if the difference between its
        # endpoints modulo nails/2 equals zero. `diagonal_skip` is nails//2.
        diagonal_skip = nails // 2

        # Input is a single line of comma-separated integers. They appear
        # interleaved so we pair consecutive values to get cords.
        data = list(map(int, data[0].split(',')))
        cords = zip(data[1:], data)
        # Count cords where (a-b) is a multiple of diagonal_skip
        result = len([(a, b) for (a, b) in cords if (a - b) % diagonal_skip == 0])

    # --- Part 2 ---
    # Count the number of crossing pairs where one endpoint lies on the
    # short arc between a and b (exclusive) and the other lies on the
    # remaining nails (i.e. the other side). The algorithm keeps a list of
    # processed cords and compares each new cord against them.
    elif part == 2:
        if sort == 'test':
            nails = 8
        else:
            nails = 256
        data = list(map(int, data[0].split(',')))
        # Here cords are ordered pairs (a,b) extracted from the interleaved list
        cords = list(zip(data[1:], data))
        result = 0
        all_cords = []
        # `all` is the set of all nail indices (1..nails)
        all = set([i for i in range(1, nails + 1)])
        for (a, b) in cords:
            # `one_side` is the set of nails strictly between a and b along
            # the numeric order (not wrapping); `remaining` are all other nails
            one_side = set([i for i in range(min(a, b) + 1, max(a, b))])
            remaining = all - one_side - set([a, b])

            # Compare this cord against all previously processed cords. If
            # one endpoint of a previous cord is in `one_side` and the other
            # in `remaining`, that pair counts as a crossing of the type we
            # are interested in.
            for (x, y) in all_cords:
                if (x in one_side and y in remaining) or (y in one_side and x in remaining):
                    result += 1
            all_cords.append((a, b))

    # --- Part 3 ---
    # This part builds a frequency map of how many times each possible cut
    # (pair of nails) is passed by cords. The cords are normalized so the
    # smaller endpoint comes first, then grouped and counted. For each
    # cord we increment counters for the cuts it crosses.
    elif part == 3:
        if sort == 'test':
            nails = 8
        else:
            nails = 256

        data = list(map(int, data[0].split(',')))
        # Normalize cords so that the lower index comes first (for counting)
        cords = sorted([(min(a, b), max(a, b)) for (a, b) in zip(data[1:], data)])

        # Initialize a dictionary of all possible cuts between nail indices
        cuts = {(a, b): 0 for a in range(1, nails + 1) for b in range(a + 1, nails + 1) if a != b}
        idx = 0
        # Walk through the sorted cords and group duplicates so we can add
        # their counts in one go (`d` is the multiplicity of the cord)
        while idx < len(cords):
            (x, y) = cords[idx]

            d = 1
            nidx = idx + 1
            # Count how many identical cords follow (multiplicity)
            while nidx < len(cords) and cords[nidx] == (x, y):
                d += 1
                nidx += 1

            # For each nail `a` strictly between x and y, consider nails `b`
            # that are strictly after y up to x + nails (wrapping around).
            # The modulus ensures `b` wraps to the 1..nails range.
            for a in range(x + 1, y):
                for b in range(y + 1, x + nails):
                    b = (b - 1) % nails + 1
                    cuts[(min(a, b), max(a, b))] += d
            # Also increment the cut that equals the cord itself
            cuts[(x, y)] += d
            idx += d
        # The result is the maximum value found among all cuts
        result = max(cuts.values())

    # Stop timing and print result with microsecond precision (rounded up)
    end = perf_counter()

    print(f"Part {part} ({ceiling((end - start) * 1000000)} micros): \t{result}")


if part == 0:
    # When `part` is 0 run all parts in sequence
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)