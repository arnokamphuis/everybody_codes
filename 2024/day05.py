from collections import defaultdict
import math
import sys

day = 5

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip().split(' ') for line in file]

def print_cols(cs):
    cc = len(cs)
    rows = max([len(c) for c in cs])
    for i in range(rows):
        row = []
        for j in range(cc):
            if i < len(cs[j]):
                row.append(str(cs[j][i]))
            else:
                row.append(' ')
        print(' '.join(row))

column_count = len(data[0])

cols = []
for c in range(column_count):
    cols.append([])

for r in range(len(data)):
    for i, v in enumerate(data[r]):
        cols[i].append(int(v))

def get_top_number(cs):
    top_row = 0
    for c in cols:
        factor = pow(10, 1+math.floor(math.log10((c[0]))))
        top_row = top_row * factor + c[0]
    
    return top_row
    
def do_round(round, cs):
    col_start = round % column_count
    number = cs[col_start].pop(0)
    col_walking = (col_start+1) % column_count
    col_length = len(cs[col_walking])
    number_place = (number-1) % (2*col_length)
    
    if number_place < col_length:
        cs[col_walking].insert(number_place, number)
    else:
        place = 2*col_length - number_place
        cs[col_walking].insert(place, number)
    return cs
        

if part == 1:
    for round in range(10):
        cols = do_round(round, cols)
    print(get_top_number(cols))
    
elif part == 2:
    round = 0
    numbers = defaultdict(int)
    while True:
        cols = do_round(round, cols)
        round = round + 1
        top_num = get_top_number(cols)
        numbers[top_num] += 1
        if numbers[top_num] == 2024:
            break

    print(top_num * round)
    
else:

    round = 0
    highest = 0
    while True:
        cols = do_round(round, cols)
        round += 1
        top_num = get_top_number(cols)
        if top_num > highest:
            highest = top_num
            print(highest)
    
