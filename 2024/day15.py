from collections import defaultdict
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
map = defaultdict(lambda: '#')
for y, line in enumerate(data):
    for x, c in enumerate(line):
        map[(x, y)] = c
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
            if map[new] == '.' or map[new] in herbs:
                queue.append((dist + 1, new))
    return distances

def key_of_min(d):
    return min(d, key = d.get)


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
    distances = defaultdict(dict)
    distances['S'][start] = bfs(start, map, herbs.keys())
    for from_herb in herbs:
        for herb_location in herbs[from_herb]:
            distances[from_herb][herb_location] = bfs(herb_location, map, herbs.keys())
    
    herbs['S'] = [start]

    # the 'circles' of water are always on the shortest track.    
    tracks = [list('SGIED'), list('DACRPN'), list('NQS')]
    location = start
    total = 0
    for track in tracks:
        min_distance = float('inf')
        from_herb = track[0]
        middle_herbs = track[1:-1]
        to_herb = track[-1]
        herb_permutations = itertools.permutations(middle_herbs)
        min_path = None
        start_loc = location
        count = 0
        
        for perm in herb_permutations:
            count += 1
            location = start_loc
            path = (from_herb,) + perm + (to_herb,)
            path_distance = 0
            for i in range(len(path) - 1):
                pds = {loc: distances[path[i]][location][loc] for loc in herbs[path[i+1]]}
                next = key_of_min(pds)
                path_distance += pds[next]
                location = next
            if path_distance < min_distance:
                min_path = path
                min_distance = path_distance
        total += min_distance
    print()
    print(total)
                        