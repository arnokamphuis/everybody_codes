from collections import defaultdict
import itertools
from math import prod
import sys

day = 17

if len(sys.argv) != 3:
    print("invalid command")
    exit()
part = int(sys.argv[1])
sort = sys.argv[2]
    
filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
with open(filename, 'r') as file:
    data = [line.strip() for line in file]

stars = []
for y, line in enumerate(data):
    for x, c in enumerate(line):
        if c == '*':
            stars.append((x+1, len(data)-y))

possible_edges = []
for a, b in itertools.combinations(stars, 2):
    d = abs(a[0] - b[0]) + abs(a[1] - b[1])
    possible_edges.append((a, b, d))

# minimal spanning tree with integer weights
# Kruskal's algorithm
def mst(edges):
    edges.sort(key=lambda x: x[2])
    parent = {}
    rank = {}
    
    def find(x):
        if x not in parent:
            parent[x] = x
            rank[x] = 0
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        rootx = find(x)
        rooty = find(y)
        if rootx == rooty:
            return False
        if rank[rootx] < rank[rooty]:
            parent[rootx] = rooty
        elif rank[rootx] > rank[rooty]:
            parent[rooty] = rootx
        else:
            parent[rooty] = rootx
            rank[rootx] += 1
        return True
    
    mst = []
    for edge in edges:
        if union(edge[0], edge[1]):
            mst.append(edge)
    return mst

edges = mst(possible_edges)

if part in [1,2]:
    print('Part {}: {}'.format(part,len(stars)+sum(edge[2] for edge in edges)))
else:
    # remove edges with the weight larger than 5
    edges = [edge for edge in edges if edge[2] <= 5]
    # group connected components in edges
    components = defaultdict(list)
    for edge in edges:
        components[edge[0]].append(edge[1])
        components[edge[1]].append(edge[0])

    count = 0
    visited = set()
    connected_components = []
    for star in stars:
        if star not in visited:
            count += 1
            cc = []
            stack = [star]
            while stack:
                node = stack.pop()
                visited.add(node)
                cc.append(node)
                for neighbor in components[node]:
                    if neighbor not in visited:
                        stack.append(neighbor)
            connected_components.append(cc)
    
    edges_in_cc = defaultdict(list)
    nodes_in_cc = defaultdict(list)
    for ccindex, cc in enumerate(connected_components):
        # find all existing edges for the connected component based on the edges list
        cc_edges = []
        for edge in edges:
            if edge[0] in cc and edge[1] in cc:
                cc_edges.append(edge)
        edges_in_cc[ccindex] = cc_edges
        nodes_in_cc[ccindex] = cc
        
    sizes = sorted([len(cc) + sum(edge[2] for edge in edges_in_cc[ccindex]) for ccindex, cc in nodes_in_cc.items()])
    print('Part {}: {}'.format(part,prod(sizes[-3:])))
