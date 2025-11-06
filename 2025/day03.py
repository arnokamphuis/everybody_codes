from copy import deepcopy
import sys

day = 3

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]

def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    crates = sorted(list(map(int,data[0].split(','))), reverse=True)
    unique_crates = sorted(set(crates), reverse=True)

    if part == 1:
        print(f"Part {part}: {sum(unique_crates)}")
    elif part == 2:
        unique_crates.reverse()
        print(f"Part {part}: {sum(unique_crates[:20])}")
    elif part == 3:
        crate_sets = []

        crate_sets.append(deepcopy(unique_crates))
        remaining_crates = deepcopy(crates)

        while True:
            for uc in unique_crates:
                remaining_crates.remove(uc)
            if not remaining_crates:
                break
            unique_crates = sorted(set(remaining_crates), reverse=True)
            crate_sets.append(deepcopy(unique_crates))
            
        print(f"Part {part}: {len(crate_sets)}")



if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)