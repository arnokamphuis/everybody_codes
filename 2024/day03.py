import sys
from copy import deepcopy
day = 3

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

def print_blocks(blcks):
    for b in blcks:
        print(''.join(list(map(lambda x: str(x), b))))
        
blocks = [ [1 if b=='#' else 0 for b in list(d)] for d in data ]

changed = True
depth = 1
while changed:
    changed = False
    old_blocks = deepcopy(blocks)
    R = len(blocks)
    C = len(blocks[0])
    dirs = [[-1,0],[1,0],[0,-1],[0,1],[0,0]] if part != 3 else [[-1,0],[1,0],[0,-1],[0,1],[1,1],[-1,1],[-1,-1],[1,-1],[0,0]]
    for r in range(1,R-1):
        for c in range(1,C-1):
            if all(d==depth for d in [old_blocks[r+dir[0]][c+dir[1]] for dir in dirs]):
                blocks[r][c] = depth+1
                changed = True
    depth = depth + 1
    
print('Part {0}: {1}'.format(part,sum([item for row in blocks for item in row])))
