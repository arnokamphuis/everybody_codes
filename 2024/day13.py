from collections import defaultdict
import sys

day = 13

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
height = defaultdict(lambda: float('inf'))
end = []
for j, line in enumerate(data):
    for i, ch in enumerate(line):
        match ch:
            case '#':
                height[(i, j)] = float('inf')
            case ' ':
                continue
            case 'E':
                start = (i, j)
                height[start] = 0
            case 'S':
                end.append((i, j))
                height[(i, j)] = 0
            case _: 
                height[(i, j)] = int(ch)
                
def get_neighbors(pos):
    x, y = pos
    return [(x + dx, y + dy) for dx, dy in directions if height[(x + dx, y + dy)] != float('inf')]

def shortest_path(start, end):
    queue = [start]
    distance = defaultdict(lambda: float('inf'))
    distance[start] = 0
    # previous = {}

    while queue:
        queue.sort(key=lambda pos: distance[pos])
        x, y = queue.pop(0)
        if (x, y) in end:
            return distance[(x,y)] #, previous
        for neighbor in get_neighbors((x, y)):
            current_height = height[(x, y)]
            neighbor_height = height[neighbor]
            distance_to_neighbor = abs(current_height - neighbor_height)
            if 10 - distance_to_neighbor < distance_to_neighbor:
                distance_to_neighbor = 10 - distance_to_neighbor
            
            distance_to_neighbor = distance_to_neighbor + 1
            if distance[neighbor] == float('inf') or distance[(x, y)] + distance_to_neighbor <= distance[neighbor]:
                # previous[neighbor] = (x, y)
                distance[neighbor] = distance[(x, y)] + distance_to_neighbor
                if neighbor not in queue:
                    queue.append(neighbor)

                
def get_path(previous, start, end):
    path = []
    current = end
    while current != start:
        path.append(current)
        current = previous[current]
    path.append(start)
    return path[::-1]

# distance, previous = shortest_path(start, end)
distance = shortest_path(start, end)
print('Part {}: {}'.format(part, distance))

if False:
    path = get_path(previous, start, end)
    grid = [[str(height[(j,i)]) if height[(j,i)] != float('inf') else data[i][j] for j in range(len(data[0]))] for i in range(len(data))]
    for x, y in path:
        grid[y][x] = 'X'
    grid[start[1]][start[0]] = 'S'
    grid[end[1]][end[0]] = 'E'
    for line in grid:
        print(''.join(line))
