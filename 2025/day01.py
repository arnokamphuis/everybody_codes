from copy import deepcopy
import sys

day = 1

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]

def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    names = data[0].split(',')
    moves = map(lambda x: (x[0],int(x[1:])), data[2].split(','))

    p = 0
    for move in deepcopy(moves):
        p += move[1] if move[0] == 'R' else -move[1]
        if part == 1:
            p = max(0, min(p, len(names)-1))
        elif part == 2:
            p %= len(names)
        else:
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