from collections import defaultdict
from copy import deepcopy
from collections import Counter
from itertools import product
from math import prod
import sys

day = 10

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [list(line.strip()) for line in file]

def base_power(ch):
    return 1 + ord(ch) - ord('A')

def intersect(a, b):
    ca = Counter(a)
    cb = Counter(b)
    ic = ca & cb
    return list(ic.elements())

def difference(a, b):
    ca = Counter(a)
    cb = Counter(b)
    ic = ca - cb
    return list(ic.elements())

def determine_runic_word(d):
    runes = [[ ' ' for _ in range(4) ] for _ in range(4)]
    hor_runes = [[] for _ in range(4)]
    ver_runes = [[] for _ in range(4)]

    for c in range (2,6):
        ver_runes[c-2] = [d[0][c], d[1][c], d[6][c], d[7][c]]
        hor_runes[c-2] = [d[c][0], d[c][1], d[c][6], d[c][7]]

    to_be_filled_in = []
    for i in range(4):
        for j in range(4):
            inter = intersect(hor_runes[i], ver_runes[j])
            if len(inter) == 1:
                runes[i][j] = inter[0]
            else:
                to_be_filled_in.append((i,j))
                runes[i][j] = '.'

    recovered = defaultdict(list)
    for tbfi in to_be_filled_in:
        i, j = tbfi
        diff = []
        if '?' in ver_runes[j]:  
            diff = difference(hor_runes[i], runes[i])

            q_index = ver_runes[j].index('?')
            if q_index >= 2:
                q_index += 4

            recovered[ (q_index, j+2) ] = diff

        elif '?' in hor_runes[i]: 
            diff = difference(ver_runes[j], [runes[x][j] for x in range(4)])

            q_index = hor_runes[i].index('?')
            if q_index >= 2:
                q_index += 4
            
            recovered[ (i+2,q_index) ] = diff
            # runes[i][j] = ch
            # recovered.append(((i,j), runes[i][j]))
            
    return ''.join([''.join([runes[i][j] for j in range(4)]) for i in range(4)]), recovered, runes

def effective_power(rw):
    return sum([base_power(ch) * (i+1) for i, ch in enumerate(rw)])
    
    
runic_word = determine_runic_word(data)

def select_rune(r, c, d):
    return [ [d[9*r+i][9*c+j] for j in range(8)] for i in range(8) ]

def select_compact_runeset(r, c, d):
    return [ [d[6*r+i][6*c+j] for j in range(8)] for i in range(8) ]

def find_heighest(s):
    powers = { x: base_power(x) for x in s }
    m = min([v for v in powers.values()])
    return [k for k,v in powers.items() if v == m][0]

def fill_in(data, r, c, unknown):
    d = deepcopy(data)
    lr, lc = unknown[0][0]
    ch = unknown[0][1]
    row = 6*r+lr
    col = 6*c+lc
    for i in range(8):
        if d[i][col] == '?':
            d[i][col] = ch
        if d[row][i] == '?':
            print(row, i, ch, d[row][i])
            d[row][i] = ch
    return d

if part == 1:
    print('Part {}: {}'.format(part, runic_word[0]))
if part == 2:
    total = 0
    R = int((len(data)+1)/9)
    C = int((len(data[0])+1)/9)
    for r in range(R):
        for c in range(C):
            total += effective_power(determine_runic_word(select_rune(r,c,data))[0])
    print('Part {}: {}'.format(part, total))
if part == 3:
    total = 0
    R = int((len(data)-2)/6)
    C = int((len(data[0])-2)/6)
    done = False
    while not done:
        all_options = defaultdict(list)
        for r in range(R):
            for c in range(C):
                sub_data = select_compact_runeset(r, c, data)
                rw, recovered, runes = determine_runic_word(sub_data)

                for i in range(4):
                    for j in range(4):
                        if runes[i][j] != '.':
                            x, y = 6*r+i+2, 6*c+j+2
                            data[x][y] = runes[i][j]
                            
                for pos, options in recovered.items():
                    i, j = pos
                    x, y = 6*r+i, 6*c+j
                    all_options[(x,y)].append(set(options))
                
        filled_in = False
        for pos, lst in all_options.items():
            filtered_lst = [l for l in lst if len(l) == 1]
            if len(filtered_lst) > 0:
                data[pos[0]][pos[1]] = list(filtered_lst[0])[0]
                filled_in = True

        done = not filled_in

    for r in range(R):
        for c in range(C):
            sub_data = select_compact_runeset(r, c, data)
            rw, _, _ = determine_runic_word(sub_data)
            if '.' not in rw:
                ep = effective_power(rw)
                total += ep

    print('Part {}: {}'.format(part, total))
