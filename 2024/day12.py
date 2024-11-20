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

if part != 3:
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

    total = 0
    for tt, twrs in towers.items():
        for tower in twrs:
            for segment, catapult in catapults.items():
                dr, dc = tower[0]-catapult[0], tower[1]-catapult[1]
                pp = (dr+dc)/3
                if int(pp)==pp:
                    sgmnum = ord(segment)-ord('A')+1
                    factor = 1 if tt == 'T' else 2
                    total += int(factor * (sgmnum * pp))
    print(total)

else:
    meteors = [[int(x) for x in line.split(' ')] for line in data]
    meteors = [ (meteor[1], meteor[0]) for meteor in meteors]

    def get_positions_projectile(start_pos, power):
        positions = [start_pos]
        positions += [(start_pos[0]+p, start_pos[1]+p) for p in range(1,power+1)]
        positions += [(positions[power][0], positions[power][1]+p) for p in range(1, power+1)]
        positions += [(positions[2*power][0]-p, positions[2*power][1]+p) for p in range(1, positions[2*power][0]+1)]
        return positions

    def get_positions_meteor(start_pos):
        return [(start_pos[0]-p, start_pos[1]-p) for p in range(start_pos[0]+1)]

    max_time = max([meteor[0] for meteor in meteors])
    print("max time", max_time)

    pp = defaultdict(dict)
    for segment, projectile in {'A':[0,0], 'B':[1,0], 'C':[2,0]}.items():
        for power in range(max_time):
            print(power)
            gpp = get_positions_projectile(projectile, power)
            for t, x in enumerate(gpp):
                if t not in pp[tuple(x)].keys():
                    pp[tuple(x)][t] = set()
                pp[tuple(x)][t].add((segment,power))

    for meteor in meteors:
        print("="*50)
        mps = get_positions_meteor(meteor)
        options = []
        for t, m in enumerate(mps):
            key = tuple(m)
            if key in pp:
                in_time = [pp[key] for tt, power in pp[key].items() if t >= tt]
                print(t, in_time)
                # print(tuple(m))
                continue
            else:
                print(" NOT ", m)
                
    # print(pp)