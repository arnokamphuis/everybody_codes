from collections import defaultdict
from copy import deepcopy
import itertools
import sys

day = 15

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

start = None
herbs = defaultdict(list)
original_map = defaultdict(lambda: '#')
for y, line in enumerate(data):
    for x, c in enumerate(line):
        original_map[(x, y)] = c
        if y == 0 and c == '.':
            start = (x, y)
        if c not in '#.~':
            herbs[c].append((x, y))

def bfs(start, map, herbs, end = None):
    queue = [(0, start)]
    distances = defaultdict(lambda: float('inf'))
    while queue:
        dist, pos = queue.pop(0)
        if end is not None and pos == end:
            return [dist]
        if pos in distances:
            continue
        distances[pos] = dist
        for dx, dy in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            new = (pos[0] + dx, pos[1] + dy)
            if new in map.keys():
                if map[new] == '.' or map[new] in herbs:
                    queue.append((dist + 1, new))
    return distances

def key_of_min(d):
    return min(d, key = d.get)

def minimal_path(herbs, distances, to_be_visited, start_herb, end_herb, remove_start = False):
    min_distance = float('inf')
    min_path = None
    
    start_location = herbs[start_herb][0]
    if remove_start:
        herbs[start_herb] = herbs[start_herb][1:]
        
    herb_permutations = itertools.permutations(to_be_visited)
    for perm in herb_permutations:
        full_path = []
        path = (start_herb,) + perm + (end_herb,)
        if remove_start:
            print(path)

        path_distance = 0
        location = start_location
        full_path.append(location)
        for i in range(len(path) - 1):
            pds = {loc: distances[path[i]][location][loc] for loc in herbs[path[i+1]]}
            next = key_of_min(pds)
            path_distance += pds[next]
            location = next
            full_path.append(location)
        if path_distance < min_distance:
            min_path = path
            min_distance = path_distance
    return min_distance, min_path, full_path
    
if part == 1:
    herb_distances = bfs(start, map, herbs.keys())
    print(2*min([herb_distances[herb] for herb in herbs['H']]))
elif part == 2:
    
    distances = defaultdict(dict)
    distances['S'][start] = bfs(start, map, herbs.keys())
    for from_herb in herbs:
        for herb_location in herbs[from_herb]:
            distances[from_herb][herb_location] = bfs(herb_location, map, herbs.keys())
    min_distance = float('inf')
    
    herb_permutations = itertools.permutations(herbs.keys())
    herbs['S'] = [start]
    min_path = None
    for perm in herb_permutations:
        path = ('S',) + perm + ('S',)
        path_distance = 0
        location = start
        for i in range(len(path) - 1):
            pds = {loc: distances[path[i]][location][loc] for loc in herbs[path[i+1]]}
            next = key_of_min(pds)
            path_distance += pds[next]
            location = next
        if path_distance < min_distance:
            min_path = path
            min_distance = path_distance
    print(min_distance)

else:
    original_map[start] = 'S'

    lmap = defaultdict(lambda: '#')
    mmap = defaultdict(lambda: '#')
    rmap = defaultdict(lambda: '#')

    location_Ks = herbs['K']
    leftKx = location_Ks[0][0] if location_Ks[0][0] < location_Ks[1][0] else location_Ks[1][0]
    rightKx = location_Ks[0][0] if location_Ks[0][0] > location_Ks[1][0] else location_Ks[1][0]

    lherbs = defaultdict(list)
    mherbs = defaultdict(list)
    rherbs = defaultdict(list)
    
    for y in range(len(data)):
        for x in range(len(data[0])):
            if x <= leftKx:
                lmap[(x, y)] = original_map[(x, y)]
                if lmap[(x, y)] not in '#~.':
                    lherbs[lmap[(x, y)]].append((x, y))
            if x >= leftKx and x <= rightKx:
                mmap[(x, y)] = original_map[(x, y)]
                if mmap[(x, y)] not in '#~.':
                    mherbs[mmap[(x, y)]].append((x, y))
            if x >= rightKx:
                rmap[(x, y)] = original_map[(x, y)]
                if rmap[(x, y)] not in '#~.':
                    rherbs[rmap[(x, y)]].append((x, y))

    mherbs['X'] = [mherbs['K'][0]]
    mherbs['K'] = [mherbs['K'][1]]
    
    ldistances = defaultdict(dict)
    for from_herb in lherbs:
        for herb_location in lherbs[from_herb]:
            ldistances[from_herb][herb_location] = bfs(herb_location, lmap, lherbs.keys())

    mdistances = defaultdict(dict)
    for from_herb in mherbs:
        for herb_location in mherbs[from_herb]:
            mdistances[from_herb][herb_location] = bfs(herb_location, mmap, mherbs.keys())
            
    rdistances = defaultdict(dict)
    for from_herb in rherbs:
        for herb_location in rherbs[from_herb]:
            rdistances[from_herb][herb_location] = bfs(herb_location, rmap, rherbs.keys())
            
    l_tbv = lherbs.keys() - {'K'}
    ll, lpath, l_fp = minimal_path(lherbs, ldistances, l_tbv, 'K', 'K')

    m_tbv = mherbs.keys() - {'K'}
    ml, mpath, m_fp = minimal_path(mherbs, mdistances, m_tbv, 'K', 'K')

    r_tbv = rherbs.keys() - {'K'}
    rl, rpath, r_fp = minimal_path(rherbs, rdistances, r_tbv, 'K', 'K')    
    
    # subtract 2 twice because the two points K are counted in all three cycles
    print(ll + ml + rl - (2 * 2))