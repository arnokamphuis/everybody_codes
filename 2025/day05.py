from copy import deepcopy
import sys
from sympy import ceiling, floor, prod
from functools import cmp_to_key

day = 5

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]

fish = [{'left': None, 'middle': None, 'right': None}]

def next_element(number, fishbone):
    if fishbone is None:
        return None
    for bone in fishbone:
        if bone['middle'] is None:
            bone['middle'] = number
            return fishbone
        elif number < bone['middle']:
            if bone['left'] is None:
                bone['left'] = number
                return fishbone
        elif number > bone['middle']:
            if bone['right'] is None:
                bone['right'] = number
                return fishbone
    new_bone = {'left': None, 'middle': number, 'right': None}
    fishbone.append(new_bone)
    return fishbone

def score_fishbone(numbers, part = 1):
    fish2 = deepcopy(fish)
    for number in numbers:
        fish2 = next_element(number, fish2)
    if part == 1:
        backbone = [bone['middle'] for bone in fish2]
        return int(''.join(map(str, backbone)))
    else:
        backbone = [bone['middle'] for bone in fish2]
        levels = []
        for bone in fish2:
            level = ""
            if bone['left'] is not None:
                level += str(bone['left'])
            level += str(bone['middle'])
            if bone['right'] is not None:
                level += str(bone['right'])
            levels.append(int(level))
        return int(''.join(map(str, backbone))), levels

def comp(a, b):
    if a[1] > b[1]:
        return -1
    elif a[1] < b[1]:
        return 1
    else:
        return b[0] - a[0] 

def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    backbone = []
    if part == 1:
        data = list(map(int,data[0].split(':')[1].split(',')))
        fish1 = deepcopy(fish)
        for number in data:
            fish1 = next_element(number, fish1)
        backbone = [bone['middle'] for bone in fish1]
        quality = ''.join(map(str, backbone))
        print(f"Part {part}: {quality}")

    elif part == 2:
        qualities = []
        for sword in data:
            numbers = list(map(int,sword.split(':')[1].split(',')))
            quality = score_fishbone(numbers)
            qualities.append(quality)
        print(f"Part {part}: {max(qualities) - min(qualities)}")

    else:
        qualities = []
        for sword in data:
            numbers = list(map(int,sword.split(':')[1].split(',')))
            quality = score_fishbone(numbers, 3)
            qualities.append((len(qualities)+1, quality))
        result = sum([ (idx+1) * id for idx, (id, _) in enumerate(sorted(qualities, key=cmp_to_key(comp)))])
        print(f"Part {part}: {result}")



if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)