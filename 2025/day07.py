from copy import deepcopy
import sys
from time import perf_counter
from sympy import ceiling, floor, prod
from functools import cmp_to_key

day = 7

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]

def run(part, sort):
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    names = data[0].split(',')
    rules = { r[0]: r[1].split(',') for r in [line.split(' > ') for line in data[2:]]}

    def check_name(name, rules):
        nz = zip(name[0:-1], name[1:])
        for f, t in nz:
            if t not in rules[f]:
                return False
        return True
    
    def count_complete_names(name, rules, result=set()):
        lastchar = name[-1]

        if lastchar in rules:
            for nextchar in rules[lastchar]:
                newname = name + nextchar
                if newname not in result:
                    if 7 <= len(newname) <= 11:
                        result.add(newname)
                    if len(newname) < 11:
                        count_complete_names(newname, rules, result)

    def count_complete_name_optimized(last, length, rules, memoization={}):
        key = (last, length)
        if key in memoization:
            return memoization[key]
        
        total = 0
        if length >= 7:
            total = 1
        if length < 11:
            if last in rules:
                for nextchar in rules[last]:
                    total += count_complete_name_optimized(nextchar, length + 1, rules, memoization)
        memoization[key] = total
        return total

    start = perf_counter() 
    result = None
    if part == 1:
        for name in names:
            if check_name(name, rules):
                result = name
        et1 = perf_counter()
    elif part == 2:
        result = 0
        for idx, name in enumerate(names, start=1):
            if check_name(name, rules):
                result += idx
    elif part == 3:
        total = 0
        filtered_names = [name for name in names if not any([name != testname and name.startswith(testname) for testname in names])]
        for name in filtered_names:
            if check_name(name, rules):
                total += count_complete_name_optimized(name[-1], len(name), rules)
        result = total

    end = perf_counter() 

    print(f"Part {part} ({ceiling((end - start) * 1000000)} micros): \t{result}")

if part == 0:
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)