import math
import sys

day = 8

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

input = int(data[0])

def build_thick_pyramid(supply, priests, acolytes, minimum):
    thickness = 1
    width = 1
    blocks = [1]
    heights = [1]
    while sum(blocks) < supply:
        thickness = (thickness * priests) % acolytes + minimum
        heights = [thickness] + [ (h + thickness) for h in heights ] + [thickness]
        width += 2
        blocks.append(thickness * width)
    return (sum(blocks) - supply) * width, heights


if part == 1:
    w = math.ceil(math.sqrt(input))
    width = w**2 - (w-1)**2
    required = (w)**2 - input

    print(required * width)
elif part == 2:
    supply = 50 if sort == "test" else 20240000
    priests = input
    acolytes = 5 if sort == "test" else 1111
    result, _ = build_thick_pyramid(supply, priests, acolytes, 0)
    print(result)
    
else:
    supply = 160 if sort == "test" else 202400000
    priests = input
    acolytes = 5 if sort == "test" else 10
    result, heights = build_thick_pyramid(supply, priests, acolytes, acolytes)
    
    width = len(heights)
    to_be_removed = [(priests * width * h) % acolytes for h in heights[1:-1]]

    print(sum(heights) - sum(to_be_removed) - supply)
