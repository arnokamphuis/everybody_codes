import sys
import statistics

day = 4

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]


nails = [int(d) for d in data]

target = 0
if part != 3:
    target = min(nails)
else:
    target = statistics.median(nails)
    
depths = [abs(d - target) for d in nails]

print('Part {0}: {1}'.format(part, int(sum(depths))))