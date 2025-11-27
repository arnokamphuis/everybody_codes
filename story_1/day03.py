from collections import deque
import sys
from time import perf_counter
from sympy import ceiling


# Day identifier used to locate input files for this puzzle/day
day = 3

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

    snail_pos = []
    for line in data:
        parts = line.split()
        parts = [int(x[2:]) for x in parts]
        snail_pos.append(parts)

    def e_gcd(a,b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = e_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    # Start a timer to measure elapsed time for this run (reported in microseconds)
    start = perf_counter()
    result = None

    # --- Part 1: return the token at (2025 mod N) ---
    if part == 1:
        result = 0
        days = 100
        for snail in snail_pos:
            period = snail[0] + snail[1] - 1
            next = days % period
            nx = 1 + (snail[0] + next - 1) % period
            ny = 1 + (snail[1] - next - 1) % period
            result += 100 * ny + nx
        pass

    # --- Part 2: map a very large turn count into the actual integer ---
    elif part == 2 or part == 3:
        states = []
        for snail in snail_pos:
            period = snail[0] + snail[1] - 1
            offset = period - snail[0]
            states.append((period, offset))

        period = states[0][0]
        remainder = states[0][1] - 1

        for p, r in states[1:]:
            n_period, n_remainder = p, r - 1
            
            rhs = n_remainder - remainder
            gcd, x, y = e_gcd(period, n_period)

            if rhs % gcd != 0:
                raise ValueError("No solution exists for the given congruences.")
            lcm_period = (period // gcd) * n_period

            k = (x * (rhs // gcd)) % (n_period // gcd)
            remainder = (period * k + remainder) % lcm_period
            period = lcm_period
        result = remainder + 1

    # --- Part 3: same mapping but with an even larger turn count ---
    # elif part == 3:
    #     pass

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