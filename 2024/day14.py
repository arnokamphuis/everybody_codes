from collections import defaultdict
import itertools
import sys

day = 14

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

def heuristic(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1]) + abs(start[2] - end[2])

def get_neighbors(pos, tree):
    x, y, z = pos
    directions = [(0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]
    return [(x + dx, y + dy, z + dz) for dx, dy, dz in directions if (x + dx, y + dy, z + dz) in tree]

def a_star(start, end, tree):
    queue = [start]
    distance = defaultdict(lambda: float('inf'))
    distance[start] = 0

    while queue:
        queue.sort(key=lambda pos: distance[pos])
        x, y, z = queue.pop(0)
        if (x, y, z) == end:
            return distance[(x, y, z)] #, previous
        for neighbor in get_neighbors((x, y, z), tree):
            if distance[neighbor] == float('inf') or distance[(x, y, z)] + 1 <= distance[neighbor]:
                distance[neighbor] = distance[(x, y, z)] + 1
                if neighbor not in queue:
                    queue.append(neighbor)

def build_tree(operations):
    tree = defaultdict(int)
    leafs = set()
    for ops in operations:
        x, y, z = 0, 0, 0
        for op in ops:
            match op[0]:
                case 'U':
                    for i in range(op[1]):
                        z += 1
                        tree[(x, y, z)] += 1
                case 'D':
                    for i in range(op[1]):
                        z -= 1
                        tree[(x, y, z)] += 1
                case 'R':
                    for i in range(op[1]):
                        x += 1
                        tree[(x, y, z)] += 1
                case 'L':
                    for i in range(op[1]):
                        x -= 1
                        tree[(x, y, z)] += 1
                case 'F':
                    for i in range(op[1]):
                        y += 1
                        tree[(x, y, z)] += 1
                case 'B':
                    for i in range(op[1]):
                        y -= 1
                        tree[(x, y, z)] += 1

        leafs.add((x,y,z))
    return tree, leafs

if part == 1:
    operations = data[0].split(',')
    operations = [(op[0], int(op[1:])) for op in operations]

    filtered = [op for op in operations if op[0] in ['U', 'D']]
    partial = list(itertools.accumulate(filtered))

    sums = [0] * len(partial)
    for index, p in enumerate(partial):
        for i in range(0, len(p), 2):
            factor = 1 if p[i][0] == 'U' else -1
            sums[index] += factor * p[i+1]

    print('Part {}: {}'.format(part, max(sums)))
elif part >= 2:
    operations = [d.split(',') for d in data]
    operations = [ [(op[0], int(op[1:])) for op in ops] for ops in operations]
    tree, leafs = build_tree(operations)             
    if part == 2:
        print('Part {}: {}'.format(part, len(tree)))
    else:
        trunk = [pos for pos in tree if pos[0] == 0 and pos[1] == 0]

        # only consider trunk segments that have a branch in any of the horizonal directions
        horizonal_directions = [(0,1,0), (0,-1,0), (1,0,0), (-1,0,0)]
        trunk = [t for t in trunk if any([tuple([t[i]+d[i] for i in range(3)]) for d in horizonal_directions if tuple([t[i]+d[i] for i in range(3)]) in tree ]) ]

        minimum_sum = 10**9
        for t in trunk:
            sum = 0
            for leaf in leafs:
                sum += a_star(leaf, t, tree)
                if sum > minimum_sum:
                    break
            if sum < minimum_sum:
                minimum_sum = sum
        print('Part {}: {}'.format(part, minimum_sum))