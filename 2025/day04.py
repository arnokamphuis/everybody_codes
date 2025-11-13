from copy import deepcopy
import sys

from sympy import ceiling, floor, prod

# Day number used to pick the input file
day = 4

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]


def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]
    factors = []
    if part != 3:
        # For parts 1 and 2 parse numbers and compute pairwise ratios
        data = list(map(int, data))
        factors = [b / a for (a, b) in list(zip(data[1:], data[:-1]))]
    else:
        # For part 3 input format differs: build tuples surrounding endpoints
        data = [(1, int(data[0]))] + [(int(a), int(b)) for [a, b] in [d.split('|') for d in data[1:-1]]] + [(int(data[-1]), 1)]
        factors = [a[1] / b[0] for (a, b) in list(zip(data[:-1], data[1:]))]

    # Product of all factors used for scaling calculations below
    upscaling = prod(factors)

    if part == 1:
        print(f"Part {part}: {floor(2025 * upscaling)}")
    if part == 2:
        print(f"Part {part}: {ceiling(10000000000000 / upscaling)}")
    if part == 3:
        print(f"Part {part}: {floor(100 * upscaling)}")


if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)