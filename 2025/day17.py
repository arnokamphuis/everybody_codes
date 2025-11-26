from collections import deque
import heapq
import sys
from time import perf_counter
from sympy import ceiling, flatten


# Module overview:
#
# This script reads a small text grid from `input/day17/...` where certain
# characters denote special locations and the remainder are numeric terrain
# costs. It supports three puzzle "parts":
#
# - Part 1: compute the total value destroyed within a radius R around an
#   `origin` point for a fixed R (simple summation over cells inside a circle).
# - Part 2: scan increasing radii to find the ring that destroys the most
#   additional value, returning a metric derived from that radius and amount.
# - Part 3: plan paths avoiding an origin-blast radius R and find a feasible
#   route under time constraints; this uses a best-first search (priority
#   queue) over a dict-based traversal graph and binary-style scanning of R.
#
# Inline comments below explain the meaning and shape of variables used.
# No algorithmic logic is changed; comments only clarify the implementation.

# Day identifier used to locate input files for this puzzle/day
day = 17

# The script expects exactly two CLI args: the part number and which input set
# to use. Typical usage examples:
#   python day13.py 1 test    # run part 1 on the 'test' input
#   python day13.py 2 real    # run part 2 on the 'real' input
if len(sys.argv) != 3:
    print("invalid command")
    exit()

# `part` chooses which puzzle/algorithm to run (1, 2 or 3 for this file)
part = int(sys.argv[1])
# `sort` chooses which input file variant to use (usually 'test' or 'real')
sort = sys.argv[2]


def run(part, sort):
    """Run the selected part using the given input variant.

    The input file is expected at `input/day{day:02d}/p{part}-{sort}.txt`.

    Note: This function focuses on explaining the algorithm; it intentionally
    does not change the original program's logic.
    """

    # Build the path to the input file and read stripped lines
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    start_pos = flatten([[(i,j) for i, v in enumerate(line) if v=='S'] for j, line in enumerate(data)])
    origin = flatten([[(i,j) for i, v in enumerate(line) if v=='@'] for j, line in enumerate(data)])
    terrain = [[d for d in line] for line in data]

    if start_pos: terrain[start_pos[1]][start_pos[0]] = '0'        
    if origin: terrain[origin[1]][origin[0]] = '0'

    terrain = [list(map(int, row)) for row in terrain]
    
    # Locate special coordinates in the input grid:
    # - `start_pos`  : coordinates of the 'S' tile (player start)
    # - `origin`     : coordinates of the '@' tile (blast origin)
    # The nested list comprehensions produce lists of (x,y) tuples; `flatten`
    # collapses them. The code expects either an empty list or a single
    # coordinate pair for each of these; the rest of the program indexes
    # them as `start_pos[0]` = x, `start_pos[1]` = y.

    # Start a timer to measure elapsed time for this run (reported in microseconds)
    start = perf_counter()
    result = None

    def destroyed(R):
        total = 0
        for y, row in enumerate(terrain):
            for x, val in enumerate(row):
                dist = (x - origin[0])**2 + (y - origin[1])**2
                if dist <= R**2:
                    total += val
        return total
    
    # Sum terrain values of all cells whose Euclidean distance from the
    # `origin` is <= R (inclusive). Distances compared using squared
    # values to avoid unnecessary sqrt calls: (dx^2 + dy^2) <= R^2.

    # --- Part 1: return the token at (2025 mod N) ---
    if part == 1:
        total = 0
        result = destroyed(10)

    # --- Part 2: map a very large turn count into the actual integer ---
    elif part == 2:
        prev = 0
        max_destroyed = 0
        max_destroyed_R = 0
        for R in range(1, min([origin[0], origin[1], len(terrain)-origin[1], len(terrain[0])-origin[0]])+1):
            result = destroyed(R)
            total = result - prev
            if total > max_destroyed:
                max_destroyed = total
                max_destroyed_R = R
            prev = result
        result = max_destroyed_R * max_destroyed
        
        # Part 2: find the radius R (scanning outwards) that yields the
        # largest incremental destroyed value (i.e., the ring [R-1,R]). We
        # compute destroyed(R) cumulatively and track the largest delta.

    # --- Part 3: same mapping but with an even larger turn count ---
    elif part == 3:

        def find_path(trn, start_pos, target_pos, origin, R):
            path = []

            dir = [(0,1),(1,0),(0,-1),(-1,0)]
            q = []
            heapq.heapify(q)
            heapq.heappush(q, (0, start_pos[0], start_pos[1], []))
            visited = set()
            while q:
                dist, c, r, p = heapq.heappop(q)
                if (c,r) in visited:
                    continue
                visited.add((c,r))
                p = p + [(c,r)]
                if (c,r) == (target_pos[0], target_pos[1]):
                    path = p
                    break
                for dc, dr in dir:
                    nc, nr = c+dc, r+dr
                    if (nc,nr) not in trn:
                        continue
                    if (origin[0]-nc)**2 + (origin[1]-nr)**2 <= R**2:
                        continue
                    heapq.heappush(q, (dist+trn[(nc,nr)], nc, nr, p))
            return path
        
        # Helper: best-first pathfinding from `start_pos` to `target_pos` on
        # a sparse traversal map `trn` (dict keyed by (x,y) -> cost). This is
        # essentially a Dijkstra/A* style search using a heap where the
        # priority is the accumulated cost. `origin` and `R` define a
        # forbidden circular region (cells inside that circle are avoided).

        left  = {(c,r): terrain[r][c] for r in range(len(terrain)) for c in range(len(terrain[0])) if c <= origin[0] or r <= origin[1]}
        right = {(c,r): terrain[r][c] for r in range(len(terrain)) for c in range(len(terrain[0])) if c >= origin[0] or r <= origin[1]}

        R = 0
        options = {}
        while True:
            max_time = 30 * (R+1)
            r = origin[1]+1+R
            path_left = find_path(left, start_pos, (origin[0], r), origin, R)
            path_right = find_path(right, (origin[0], r), start_pos, origin, R)
            path = path_left + path_right[1:]
            time_taken = sum([terrain[r][c] for c,r in path])
            if time_taken < max_time:
                result = R * time_taken
                break

            R += 1
            if R >= min([origin[0], origin[1], len(terrain)-origin[1], len(terrain[0])-origin[0]]):
                break
        
        # Incrementally increase forbidden radius R until a feasible round
        # trip is found that meets the time constraint `max_time`.

    # Stop timing and print result with microsecond precision (rounded up)
    end = perf_counter()
    print(f"Part {part}: ({int(ceiling((end - start) * 1000000)):>12} microseconds): \t{result}")


if part == 0:
    # Convenience mode: run all parts in sequence
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)