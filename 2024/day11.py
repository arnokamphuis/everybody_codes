from collections import defaultdict
from copy import deepcopy
import sys

day = 11

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

rules = [line.split(':') for line in data]
rules = { rule[0]: rule[1].split(',') for rule in rules}

def day(p):
    new_population = defaultdict(int)

    for species, count in p.items():    
        rule = rules[species]
        for s in rule:
            new_population[s] += count
    
    return new_population


if part == 1:
    population = {'A': 1 }
    for _ in range(4):
        population = day(population)
    print(sum([v for v in population.values()]))
elif part == 2:
    population = {'Z': 1 }
    for _ in range(10):
        population = day(population)
    print(sum([v for v in population.values()]))
else:
    populations = {species: defaultdict(int) for species in rules.keys()}
    for species in populations.keys():
        populations[species][species] = 1
        for generation in range(20):
            populations[species] = day(populations[species])
    pop_sizes = [sum([v for v in pop.values()]) for pop in populations.values()]
    print(max(pop_sizes) - min(pop_sizes))