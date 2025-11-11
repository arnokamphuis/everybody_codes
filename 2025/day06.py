from copy import deepcopy
import sys
from sympy import ceiling, floor, prod
from functools import cmp_to_key

day = 6

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]

def find_pairs(knight, novice, data):
    knights = [1 if d == knight else 0 for d in data]
    novices = [1 if d == novice else 0 for d in data]
    ks = 0
    pairs = 0
    for k, n in zip(knights, novices):
        if k == 1:
            ks += 1
        if n == 1:
            pairs += ks
    return pairs


def find_pairs_long(knight, novice, data, repeats, width):

    total_length = len(data) * repeats

    knights = [1 if d == knight else 0 for d in data]
    novices = [1 if d == novice else 0 for d in data]


    knight_count = 0
    for idx in range(0, min(width, total_length-1)+1):
        if knights[idx % len(data)] == 1:
            knight_count += 1

    pairs = 0
    for i in range(0, total_length):
        index = i % len(data)

        if novices[index] == 1:
            pairs += knight_count

        left = i - width
        if left >=0:
            if knights[left % len(data)] == 1:
                knight_count -= 1
        right = i + 1 + width
        if right < total_length:
            if knights[right % len(data)] == 1:
                knight_count += 1

    return pairs

def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file][0]

    pairs = 0
    if part == 1:
        pairs += find_pairs('A', 'a', data)
    elif part == 2:
        pairs += find_pairs('A', 'a', data)
        pairs += find_pairs('B', 'b', data)
        pairs += find_pairs('C', 'c', data)
    elif part == 3:
        if sort == 'test':
            # width = 10
            # repeats = 2
            width = 1000
            repeats = 1000
        else:
            width = 1000
            repeats = 1000

        As = find_pairs_long('A', 'a', data, repeats, width)
        Bs = find_pairs_long('B', 'b', data, repeats, width)
        Cs = find_pairs_long('C', 'c', data, repeats, width)
        pairs += As + Bs + Cs
    
    print(f"Part {part}: {pairs}")



if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)