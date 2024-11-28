from collections import defaultdict
import itertools
import sys

day = 18

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

palms = set()
garden = set()
entries = set()
for y, line in enumerate(data):
    if y == 0:
        if '.' in line:
            entries.add((line.index('.'), 0))
    elif y == len(data) - 1:
        if '.' in line:
            entries.add((line.index('.'), y))
    else:
        if line[0] == '.':
            entries.add((0, y))
        elif line[-1] == '.':
            entries.add((len(line) - 1, y))
            
    for x, c in enumerate(line):
        match c:
            case '.':
                garden.add((x, y))
            case 'P':
                garden.add((x, y))
                palms.add((x, y))
            case _:
                continue

def water_garden(start_points):
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    water_front = start_points.copy()

    visited = set()
    visited.update(start_points)
    palms_watered = set()
    
    t = 0
    done = False
    while not done:
        t += 1
        new_front = set()
        for x, y in water_front:
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (nx, ny) in garden and (nx, ny) not in visited:
                    if (nx, ny) in palms:
                        palms_watered.add((nx, ny))
                        if len(palms_watered) == len(palms):
                            done = True
                            break
                    new_front.add((nx, ny))
                    visited.add((nx, ny))
        water_front = new_front
    return t               
    
    
if part == 1 or part == 2:
    print('Part {}: {}'.format(part,water_garden(entries)))
else:
    def bfs(start_pos):
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        visited = defaultdict(int)
        visited[start_pos] = 0
        queue = [(start_pos, 0)]
        while queue:
            pos, t = queue.pop(0)
            for dx, dy in directions:
                nx, ny = pos[0] + dx, pos[1] + dy
                if (nx, ny) in garden and (nx, ny) not in visited.keys():
                    visited[(nx, ny)] = t + 1
                    queue.append(((nx, ny), t + 1))
        return visited
    
    distances = defaultdict(dict)
    for palm in palms:
        distances[palm] = bfs(palm)
    
    print('Part {}: {}'.format(part,min([sum([distances[palm][pos] for palm in palms]) for pos in garden if pos not in palms])))
