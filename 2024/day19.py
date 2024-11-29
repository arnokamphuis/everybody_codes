from collections import defaultdict
from copy import deepcopy
import itertools
import sys

day = 19

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

rotations = list(data[0])

message_grid = [list(line) for line in data[2:]]

def find_cycle_in_positions(R, C, operations):
    dir = {'R': 1, 'L': -1}
    indices = [(-1, -1), (-1,  0), (-1,  1), ( 0,  1), ( 1,  1), ( 1, 0), ( 1,  -1), ( 0,  -1)]

    op_index = 0
    index_grid = [[(i,j) for j in range(C)] for i in range(R)]
    
    for rr in range(1,R-1):
        for cc in range(1,C-1):            
            delta_index = dir[operations[op_index % len(operations)]]
            original_index_grid = [[index_grid[rr+i][cc+j] for j in range(-1,2)] for i in range(-1,2)]
            new_indices = [indices[(i+delta_index) % 8] for i in range(8)]            
            for (fr, fc), (tr, tc) in zip(indices, new_indices):
                index_grid[rr+tr][cc+tc] = original_index_grid[fr+1][fc+1]
            op_index += 1
            
    transition = {}
    for r in range(R):
        for c in range(C):
            transition[index_grid[r][c]] = (r, c)
            
    cycles = []
    seen = set()
    for sr in range(R):
        for sc in range(C):
            if (sr, sc) in seen: continue
            cycle = []
            r, c = sr, sc
            while (r, c) not in seen:
                cycle.append((r,c))
                seen.add((r,c))
                r, c = transition[r, c]
            cycles.append(cycle)
    return cycles            

def perform(grid, operations, rounds):
    R, C = len(grid), len(grid[0])
    cycles = find_cycle_in_positions(R, C, operations)

    newgrid = deepcopy(grid)
    for cycle in cycles:
        for i, (sr,sc) in enumerate(cycle):
            dr, dc = cycle[(i+rounds) % len(cycle)]
            newgrid[dr][dc] = grid[sr][sc]
    return newgrid

def get_message_from_grid(grid):
    result_msg = ''.join([''.join(line) for line in grid])
    return result_msg[result_msg.index('>')+1:result_msg.index('<')]

number_of_cycles = {1: 1, 2: 100, 3: 1048576000}
message_grid = perform(message_grid, rotations, number_of_cycles[part])
print('Part {}: {}'.format(part,get_message_from_grid(message_grid)))
