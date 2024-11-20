from collections import defaultdict
import sys

day = 12

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

base = len(data)-2
towers = defaultdict(list)
catapults = defaultdict(tuple)
for i, line in enumerate(data):
    for j, ch in enumerate(line):
        match ch:
            case 'A'|'B'|'C':
                catapults[ch] = (base-i,j)
            case 'T'|'H':
                towers[ch].append((base-i,j))
            case _:
                continue
# towers = sorted(towers, key=lambda tower: tower[0], reverse=True)
total = 0
for tt, twrs in towers.items():
    for tower in twrs:
        for segment, catapult in catapults.items():
            dr, dc = tower[0]-catapult[0], tower[1]-catapult[1]
            pp = (dr+dc)/3
            if int(pp)==pp:
                print('raak', int(pp), segment)
                sgmnum = ord(segment)-ord('A')+1
                factor = 1 if tt == 'T' else 2
                total += factor * (sgmnum * pp)
            
        # print(segment, tower, dr, dc)
        continue
            
print(dict(catapults))
print(dict(towers))
print(total)