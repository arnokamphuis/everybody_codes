import sys

day = 1

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

input = data[0]
potions_required = {'A': 0, 'B': 1, 'C': 3, 'D': 5, 'x': -1}

def total_required(p):
    pf = list(filter(lambda x: x >= 0, list(p)))
    match len(pf):
        case 1: 
            return sum(pf)
        case 2: 
            return sum(pf) + 2
        case 3: 
            return sum(pf) + 6
        case _: 
            return 0

potions_needed = [ [potions_required[c] for c in input[i:i+part]] for i in range(0, len(input), part)]
print('Part {0}: {1}'.format(part, sum(list(map(lambda p: total_required(p), potions_needed)))))
