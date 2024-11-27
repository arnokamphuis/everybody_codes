from collections import defaultdict
from functools import reduce
import itertools
from math import gcd
import sys

day = 16

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line for line in file]

turns = [int(d) for d in data[0].split(',')]

number_of_rolls = len(turns)

rolls = [[] for i in range(number_of_rolls)]

symbols = set()

for roll_number in range(number_of_rolls):
    for i in range(2, len(data)):
        code = data[i][4*roll_number:4*roll_number+3]
        if ' ' not in code and len(code)==3:
            symbols = symbols.union(set(code))
            rolls[roll_number].append(code)

current_positions = [0 for i in range(number_of_rolls)]

def get_code(turn):
    finished_position = [ (turn * turns[i]) % len(rolls[i]) for i in range(number_of_rolls) ]
    return ' '.join([rolls[i][finished_position[i]] for i in range(number_of_rolls)])

def lcm(a, b):
    return a * b // gcd(a, b)

def lcm_of_list(numbers):
    return reduce(lcm, numbers)

def calculate_min_turns(turns, size_rolls):
    # Calculate the LCM of size_rolls and turns combined
    advances = [size_rolls[i] * turns[i] for i in range(len(turns))]
    return reduce(lcm, advances)

def symbol_counts(code, symbol = None):
    if symbol:
        return code.count(symbol)
    else:
        return [code.count(s) for s in symbols]

def coins_in_turn(turn):
    return coins_in_code(get_code(turn))

def coins_in_code(code):
    code = code[::2]
    sc = symbol_counts(code)
    triplets = [1 if sc[i] >= 3 else 0 for i in range(len(sc))]
    extras = [sc[i] - 3 if sc[i] > 3 else 0 for i in range(len(sc))]
    return sum(triplets) + sum(extras)

def get_code_from_positions(pos):
    return ' '.join([rolls[i][pos[i] % len(rolls[i])] for i in range(number_of_rolls)])

if part == 1:
    print('Part {}: {}'.format(part, get_code(100)))
if part == 2:       
    total_pulls = 202420242024

    pulls = lcm_of_list([len(r) for r in rolls])    
    current_coins = 0
    total_coins = 0
    for i in range(0, pulls + (total_pulls % pulls)):
        if i == pulls:
            total_coins += current_coins * (total_pulls // pulls)
            current_coins = 0
        current_coins += coins_in_turn(i)
    print('Part {}: {}'.format(part, total_coins+current_coins))
    
elif part == 3:
        
    DP = { 'max': {}, 'min': {} }
    
    def get_total_coins(pos, pull, find_func):
        key = (tuple(pos), pull)
        if key in DP[find_func.__name__]:
            return DP[find_func.__name__][key]
        
        if pull == 0:
            return 0
        
        options = []
        for d in [-1,0,1]:
            new_pos = [ (pos[i] + turns[i] + d) % len(rolls[i]) for i in range(number_of_rolls) ]
            coins = coins_in_code(get_code_from_positions(new_pos))
            coins += get_total_coins(new_pos, pull - 1, find_func)
            options.append(coins)
        extreme = find_func(options)
        
        DP[find_func.__name__][key] = extreme
        return extreme
    
    total_pulls = 256
    positions = [0 for i in range(number_of_rolls)]
    
    print('Part {}: {} {}'.format(part, get_total_coins(positions, total_pulls, max), get_total_coins(positions, total_pulls, min)))
