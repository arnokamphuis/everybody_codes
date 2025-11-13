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

# A simple tree-like structure: each node (a "bone") can have left/middle/right
fish = [{'left': None, 'middle': None, 'right': None}]


def next_element(number, fishbone):
    # Insert `number` into the first available slot in the list-of-nodes
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
    # If no slot found, append a new bone with `number` as its middle
    new_bone = {'left': None, 'middle': number, 'right': None}
    fishbone.append(new_bone)
    return fishbone


def score_fishbone(numbers, part=1):
    # Build a fishbone (list of bones) and produce combined numeric "quality"
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


def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    backbone = []
    if part == 1:
        # Input lines like "name:1,2,3", parse the list and create fish1
        data = list(map(int, data[0].split(':')[1].split(',')))
        fish1 = deepcopy(fish)
        for number in data:
            fish1 = next_element(number, fish1)
        backbone = [bone['middle'] for bone in fish1]
        quality = ''.join(map(str, backbone))
        print(f"Part {part}: {quality}")

    elif part == 2:
        # Evaluate the quality for each sword line and return the range
        qualities = []
        for sword in data:
            numbers = list(map(int, sword.split(':')[1].split(',')))
            quality = score_fishbone(numbers)
            qualities.append(quality)
        print(f"Part {part}: {max(qualities) - min(qualities)}")

    else:
        # For the final part compute a weighted ranking across sword qualities
        qualities = []
        for sword in data:
            numbers = list(map(int, sword.split(':')[1].split(',')))
            quality = score_fishbone(numbers, 3)
            qualities.append((quality, (len(qualities) + 1)))
        qualities.sort(reverse=True)

        result = sum([idx * id for idx, (_, id) in enumerate(qualities, start=1)])
        print(f"Part {part}: {result}")


if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)