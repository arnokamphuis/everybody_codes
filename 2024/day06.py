from collections import defaultdict
import sys
from copy import deepcopy

day = 6

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

branches = { d.split(':')[0]: d.split(':')[1].split(',') for d in data }

def walk_tree(path_up_to_now, bs):
    last_in_path = path_up_to_now[-1]
    if last_in_path == '@':
        return [path_up_to_now]

    next = bs[last_in_path]
    all_paths = []
    for n in next:
        if n in path_up_to_now:
            continue
        if n in bs.keys() or n == '@':
            putn = deepcopy(path_up_to_now) + [n]
            all_paths += walk_tree(putn, bs)
    return all_paths
paths = walk_tree(['RR'], branches)
lengths = defaultdict(list)
for p in paths:
    lengths[len(p)].append(p)
branch = [v[0] for k,v in lengths.items() if len(v)==1][0]

if part == 1:
    print(''.join(branch))
else:
    print(''.join([b[0] for b in branch]))
