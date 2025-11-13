from copy import deepcopy
import sys
from time import perf_counter
from sympy import ceiling, floor, prod
from functools import cmp_to_key

day = 8

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]

def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    start = perf_counter() 
    result = None

    if part == 1:
        if sort == 'test':
            nails = 8
        else:
            nails = 32
        diagonal_skip = nails//2

        data = list(map(int, data[0].split(',')))
        cords = zip(data[1:], data)
        result = len([(a,b) for (a,b) in cords if (a-b)%diagonal_skip == 0])
    elif part == 2:
        if sort == 'test':
            nails = 8
        else:
            nails = 256
        data = list(map(int, data[0].split(',')))
        cords = list(zip(data[1:], data))
        result = 0
        all_cords = []
        all = set([i for i in range(1,nails+1)])
        for (a,b) in cords:
            one_side = set([i for i in range(min(a,b)+1, max(a,b))])
            remaining = all - one_side - set([a,b])

            for (x,y) in all_cords:
                 if (x in one_side and y in remaining) or (y in one_side and x in remaining):
                    result += 1
            all_cords.append((a,b))
    elif part == 3:
        if sort == 'test':
            nails = 8
        else:
            nails = 256
        data = list(map(int, data[0].split(',')))
        cords = list(zip(data[1:], data))
        result = 0
        all = set([i for i in range(1,nails+1)])
        for a,b in set([(a,b) for a in range(1,nails+1) for b in range(a+1,nails+1) if a != b]):
            one_side = set([i for i in range(min(a,b)+1, max(a,b))])
            remaining = all - one_side - set([a,b])
            result = max(result, len([(x,y) for (x,y) in cords if (x in one_side and y in remaining) or (y in one_side and x in remaining) or (set([x,y]) == set([a,b]))]))
    end = perf_counter() 

    print(f"Part {part} ({ceiling((end - start) * 1000000)} micros): \t{result}")

if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)