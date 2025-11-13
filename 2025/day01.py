from copy import deepcopy
import sys

# Day identifier used to locate corresponding input files
day = 1

# Expect two CLI args: part and input variant (e.g. `test` or `real`)
if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]


def run(part, sort):
    # Load input for this day/part/sort
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    # Names on a list and a sequence of moves like R3 or L2
    names = data[0].split(',')
    moves = map(lambda x: (x[0], int(x[1:])), data[2].split(','))

    # `p` is the current position/index used differently per part
    p = 0
    for move in deepcopy(moves):
        # Move right increases index, left decreases
        p += move[1] if move[0] == 'R' else -move[1]
        if part == 1:
            # Clamp within bounds for part 1
            p = max(0, min(p, len(names) - 1))
        elif part == 2:
            # Wrap around for part 2
            p %= len(names)
        else:
            # For part 3 swap selected name into first position
            p %= len(names)
            names[0], names[p] = names[p], names[0]
            p = 0
    print(f"Part {part}: {names[p]}")


if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)