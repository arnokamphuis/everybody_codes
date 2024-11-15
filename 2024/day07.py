from copy import deepcopy
import itertools
import sys

day = 7

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]
    
index = [i for i in range(len(data)) if data[i]=='']

def find_track(field):
    R, C = len(field), len(field[0])
    track = []
    s, cd = [0,0], 0
    pnp = [0,0]
    cp = s
    dirs = {0: [1,0], 1: [0,1], 2: [-1,0], 3: [0,-1]}
    dir_change = [0, -1, 1]
    d = dirs[cd]
    cp[0], cp[1] = cp[0]+d[0], cp[1]+d[1]
    next = field[cp[1]][cp[0]]
    while next != 'S':
        track.append(next)
        
        for dc in dir_change:
            ncd = (cd + dc)%4
            if ncd < 0:
                ncd += 4
            nd = dirs[ncd]
            pnp[0] = cp[0] + nd[0]
            pnp[1] = cp[1] + nd[1]
            if pnp[1] >= 0 and pnp[1] < R and pnp[0] >=0 and pnp[0] < len(field[pnp[1]]):
                if field[pnp[1]][pnp[0]] != ' ':
                    cd = ncd
                    break
        d = dirs[cd]
        cp[0], cp[1] = cp[0]+d[0], cp[1]+d[1]
        next = field[cp[1]][cp[0]]
    track.insert(0,'S')
    return track

DP = {}

def score_one_loop(step, ops, track):
    power = 0
    power_used = 0    
    key = (step % len(ops), tuple(ops))
    if key in DP:
        return DP[key]
    
    for s in range(1,len(track)+1):
        t = track[s%len(track)]
        if t == '+':
            power += 1
        elif t == '-':
            power -= 1
        else:
            match ops[step % len(ops)]:
                case '+':
                    power += 1
                case '-':
                    power -= 1
                case '=':
                    power = power
                case _:
                    assert(False)
        power_used += power
        step += 1

    DP[key] = (power_used, power)
    return (power_used, power)    

def score_knight(ops, rounds, track):
    power = 10
    power_used = 0
    step = 0
    for _ in range(rounds):
        (pu, p) = score_one_loop(step, ops, track)
        power_used += pu + power*len(track)
        power += p
        step = (step+len(track)) % len(ops)
    return power_used


if part == 1:
    operations = { d.split(':')[0]: d.split(':')[1].split(',') for d in data }

    power = { k: 10 for k in operations.keys() }
    power_used = { k: 0 for k in operations.keys() }

    for round in range(10):
        for device, ops in operations.items():
            match ops[round % len(ops)]:
                case '+':
                    power[device] += 1
                case '-':
                    power[device] -= 1
                case '=':
                    power[device] = power[device]
                case _:
                    assert(False)
            
            power_used[device] += power[device]

    print(''.join([k for k, v in sorted(power_used.items(), key=lambda item: item[1], reverse=True)]))
else:
    assert(len(index) > 0)
    operations = { d.split(':')[0]: d.split(':')[1].split(',') for d in data[0:index[0]] }

    power = { k: 10 for k in operations.keys() }
    power_used = { k: 0 for k in operations.keys() }
        
    field = data[index[0]+1:]
    track = find_track(field)

    loops = 10 if part == 2 else 2024
    for device, ops in operations.items():
        power_used[device] = score_knight(ops, loops, track)
    if part == 2:
        print(''.join([k for k, v in sorted(power_used.items(), key=lambda item: item[1], reverse=True)]))    
    else:
        target_score = power_used['A']
        
        count = 0
        options = set(itertools.permutations('+++++---==='))
        for i, option in enumerate(options):
            option_score = score_knight(option, loops, track)
            if option_score > target_score:
                count += 1
        print(count)

