from collections import deque
from copy import deepcopy
from math import prod
import sys
from time import perf_counter
from sympy import ceiling


# Module overview and purpose:
#
# This script processes a small puzzle input (a single line of comma-separated
# integers) and computes results for three related parts. The computations
# involve basic number theory (GCD/LCM), a domain-specific ``factorize``
# decomposition, and searching for bounds using exponential + binary search.
#
# Inline comments below explain the helper functions and the algorithmic
# steps taken in each puzzle part. No functional behavior is changed.

# Day identifier used to locate input files for this puzzle/day
day = 16

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

    Note: This function focuses on explaining the algorithm; it intentionally
    does not change the original program's logic.
    """

    # Build the path to the input file and read stripped lines
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    # Compute greatest common divisor (GCD) using Euclid's algorithm.
    # Used by `lcm` for pairwise least-common-multiple computations.
    def gcd(a, b):
        """Return greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a
    
    def lcm(a, b):
        """Return least common multiple of a and b.

        Uses lcm(a,b) = |a*b| // gcd(a,b). The integer division is exact
        because gcd divides the product.
        """
        return a * b // gcd(a, b)
    
    # Determine the minimal repeating cycle (LCM of all periods in `list`).
    # For a collection of periods, the LCM gives the smallest time after
    # which all periodic events align again.
    def determine_minimal_cycle(list):
        multiple = list[0]
        for num in list[1:]:
            multiple = lcm(multiple, num)
        return multiple
    
    # Decompose the input vector `nums` into factor sizes.
    #
    # This routine finds the smallest index `n` such that `nums[n-1] == 1`,
    # appends `n` to the factor list, and then subtracts 1 from every
    # position whose index is a multiple of n. The process repeats until
    # all entries are <= 0. The exact meaning is domain-specific to the
    # puzzle but effectively yields a multiset of divisors/factors used
    # by later computations.
    def factorize(nums):
        factors = []
        while True:
            found = False
            # find first n with value exactly 1
            for n in range(1, len(nums) + 1):
                if (nums[n - 1] == 1):
                    factors.append(n)
                    found = True
                    break
            if found:
                # for every multiple of n, subtract one (consume that slot)
                for idx in range(n, len(nums) + 1, n):
                    if nums[idx - 1] > 0:
                        nums[idx - 1] -= 1

            # stop when all positions are accounted for (zero or negative)
            if all(x <= 0 for x in nums):
                break
        return factors
    
    numbers = [int(x) for x in data[0].split(",")]

    # Start a timer to measure elapsed time for this run (reported in microseconds)
    start = perf_counter()
    result = None

    # --- Part 1: return the token at (2025 mod N) ---
    if part == 1:
        # Part 1: count how many (position,n) pairs satisfy position % n == 0
        # for positions in 1..90. This is a straightforward brute-force count
        # used in the first puzzle part.
        count = 0
        for position in range(1, 90 + 1):
            for n in numbers:
                # increment when position is an exact multiple of n
                count += ((position % n) == 0)
        result = count
        # The minimal repeating cycle (LCM of numbers) can also be computed
        # via determine_minimal_cycle(numbers), but it's not required here.

    
    # --- Part 2: map a very large turn count into the actual integer ---
    elif part == 2:
        # Part 2: factorize a copy of the input and return the product of
        # the discovered factor sizes. We deep-copy `numbers` since
        # `factorize` mutates its input.
        result = prod(factorize(deepcopy(numbers)))


    # --- Part 3: same mapping but with an even larger turn count ---
    elif part == 3:

        # Count how many "blocks" are covered by an integer n given the
        # discovered `factors`. Each factor f contributes floor(n/f) blocks.
        def determine_blocks_needed(n, factors):
            total = 0
            for f in factors:
                total += n // f
            return total

        # Problem-specific large target value; the algorithm finds the
        # maximal `n` such that cumulative blocks remain below this target.
        total_blocks = 202520252025000

        # get factor sizes (factorize mutates the array, so copy)
        factors = factorize(deepcopy(numbers))

        # Exponential search to find an upper bound `n` where the number of
        # blocks exceeds `total_blocks`. Doubling ensures we find a bound in
        # O(log N) doublings where N is the desired n.
        n = 1
        while True:
            n *= 2
            dbn = determine_blocks_needed(n, factors)
            if dbn > total_blocks:
                break

        # Binary search in (n/2, n] to find the largest value `low` for which
        # determine_blocks_needed(low) < total_blocks. The loop terminates
        # with `low` being that threshold.
        low = n // 2
        high = n
        while low + 1 < high:
            mid = (low + high) // 2
            dbn = determine_blocks_needed(mid, factors)
            if dbn < total_blocks:
                low = mid
            else:
                high = mid

        result = low


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