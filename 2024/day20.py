from collections import defaultdict
import itertools
import sys

day = 20

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]


start = None
cur_dir = (1, 0)
all_directions = [(1, 0), (0, -1), (-1, 0), (0, 1)]

R, C = len(data), len(data[0])

map = defaultdict(int)
checkpoints = defaultdict(str)
for r in range(len(data)):
    for c in range(len(data[0])):
        match data[r][c]:
            case '.':
                map[(r, c)] = -1
            case '-':
                map[(r, c)] = -2
            case '+':
                map[(r, c)] = +1
            case 'S':
                map[(r, c)] = -1
                start = (r, c)
            case _:
                if data[r][c] == '#':
                    continue
                else:
                    map[(r, c)] = -1
                    checkpoints[(r,c)] = data[r][c]

cps_values = sorted(checkpoints.values())
checkpoints = {k: cps_values.index(v)  for k, v in checkpoints.items()}

def get_possible(pos, dir):
    r, c = pos
    pnindex = [all_directions.index(dir)]
    pnindex.append((pnindex[0] + 1) % 4)
    pnindex.append((pnindex[0] + 3) % 4)
    possible_directions = [all_directions[i] for i in pnindex]
    
    for dr, dc in possible_directions:
        if (r + dr, c + dc) in map: # no solid object
            yield (r + dr, c + dc), (dr, dc)

if part == 1:
    states = {(start, d): 1000 for d in all_directions}
    for _ in range(100):
        new_states = {}
        for (pos, dir), height in states.items():
            for next_pos, next_dir in get_possible(pos, dir):
                next_height = height + map[next_pos]
                key = (next_pos, next_dir)
                if key in new_states:
                    new_states[key] = max(new_states[key], next_height)
                else:
                    new_states[key] = next_height
        states = new_states
    print('Part {}: {}'.format(part,max(states.values())))
elif part == 2:
    states = {(start, d, 0): 10000 for d in all_directions}
    done = False
    t = 0
    while not done:
        t += 1
        new_states = {}
        for (pos, dir, cps), height in states.items():
            for next_pos, next_dir in get_possible(pos, dir):
                next_height = height + map[next_pos]
                next_cps = cps
                if next_pos == start and next_height >= 10000 and cps == len(checkpoints):
                    done = True
                    break
                if next_pos in checkpoints:
                    p_cps = checkpoints[next_pos]
                    if p_cps == cps:
                        next_cps = cps + 1
                key = (next_pos, next_dir, next_cps)
                if key in new_states:
                    new_states[key] = max(new_states[key], next_height)
                else:
                    new_states[key] = next_height
        states = new_states
    print('Part {}: {}'.format(part,t))
    
else:
    
    distance = 0
    height = 384400
    
    def key_of_max(d):
        return max(d, key = d.get)
    def key_of_min(d):
        return min(d, key = d.get)

    columns = {}
    for c in range(C):
        if all([(r,c) in map for r in range(R)]):
            columns[c] = sum([map[(r,c)] for r in range(R)])
    min_delta = max(columns.values())
    best_column = key_of_min({k: abs(start[1]-k) for k, v in columns.items() if v == min_delta})
    distance_to_best = abs(start[1] - best_column)
    
    height -= min(distance_to_best, height)
    
    while height > R:
        height += sum([map[(r,best_column)] for r in range(R)])
        distance += R

    if height > 0:
        index = 0
        while height > 0:
            distance += 1
            index += 1
            height += map[(index%R,best_column)]

    print('Part {}: {}'.format(part, distance ))
