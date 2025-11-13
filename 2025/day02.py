from copy import deepcopy
import sys

day = 2

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]


def add(x, y):
    # Complex-plane style addition on [real, imag] pairs
    return [x[0] + y[0], x[1] + y[1]]


def mult(x, y):
    # Multiply two complex numbers represented as [r, i]
    return [x[0] * y[0] - x[1] * y[1], x[0] * y[1] + x[1] * y[0]]


def div(x, y):
    # Integer division on each component (used sparingly in this code)
    return [x[0] // y[0], x[1] // y[1]]


def cycle(R, A, part):
    # Update rule used repeatedly. The `factor` changes depending on part.
    factor = 10 if part == 1 else 100000
    return [int((R[0] * R[0] - R[1] * R[1]) / factor) + A[0], int((2 * R[0] * R[1]) / factor) + A[1]]


def in_range(P):
    # Check if both coordinates are within a large bounding box
    return P[0] > -1000000 and P[0] < 1000000 and P[1] > -1000000 and P[1] < 1000000


def run(part, sort):
    # Load input and parse the anchor point A from the first line
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    R = [0, 0]

    # Parse the A coordinate from a string like 'A=(x,y)'
    A = list(map(int, data[0][3:-1].split(',')))

    if part == 1:
        # Run the cycle a few times and print the result
        R = cycle(R, A, part)
        R = cycle(R, A, part)
        R = cycle(R, A, part)
        print(f"Part {part}: {R}")
    else:
        # For other parts we scan a grid of candidate points and check
        # whether repeated cycles remain in-range; coarser sampling for
        # non-precise runs (step=10) vs precise (step=1 for part 3)
        count = 0
        points = set()
        for y in range(A[1], A[1] + 1001, 1 if part == 3 else 10):
            for x in range(A[0], A[0] + 1001, 1 if part == 3 else 10):
                count += 1
                all_in_range = True
                P = [x, y]
                R = [0, 0]
                for _ in range(100):
                    R = cycle(R, P, part)
                    all_in_range = all_in_range and in_range(R)
                    if not all_in_range:
                        break
                if all_in_range:
                    points.add((x, y))

        print(f"Part {part}: {len(points)} points found ({count} checked)")


if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)