from collections import defaultdict, deque
from operator import pos
import sys
from time import perf_counter
from sympy import ceiling
import heapq

# Detailed comments added throughout to explain the algorithm and data structures.
#
# High level summary:
# - This script parses a sequence of turning-and-stepping instructions (e.g. "R2,L3,...")
#   describing movement on an integer grid starting from (0,0) facing north.
# - It constructs a compacted representation of the visited path and a surrounding
#   grid (with a small padding) by mapping real coordinates to a denser index-space.
# - Walls are marked on the compacted grid wherever the path overlaps grid lines
#   (these represent barriers in the dungeon). The task is to compute the shortest
#   path length from the start to the final position (i.e., navigate around walls).
#
# Key functions:
# - build_intervals: determine relevant x/y coordinates (points-of-interest),
#   build a mapping between real coordinates and compacted grid indices, and
#   initialize a dungeon grid (dictionary keyed by index pairs) with all cells open.
# - on_line: helper that tests whether a given compacted grid cell lies on a
#   specific axis-aligned segment in real coordinates.
# - find_shortest_path_length: A* (priority queue) over compacted grid cells
#   to compute Manhattan-distance based shortest path between start and goal.
# - build_dungeon: convert movement instructions into wall cells on the compacted
#   grid then delegate to the pathfinder to get the shortest path length.
# Day identifier used to locate input files for this puzzle/day
day = 15

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

    data = data[0].split(',')
    data = [(d[0], int(d[1:])) for d in data]

    # placeholder; the real `dungeon` structure is created by helpers
    dungeon = set()

    # Start a timer to measure elapsed time for this run (reported in microseconds)
    start = perf_counter()
    result = None

    # map maps from index to real coordinate
    # rev_map maps from real coordinate to index

    def build_intervals(instructions):
        # current real-coordinate position (x, y)
        pos = (0, 0)
        # current facing direction vector; (0,1) = north/up
        dir = (0, 1)
        horizontal_PoI = set()
        vertical_PoI = set()

        # include starting row/column as points-of-interest
        horizontal_PoI.add(pos[1])
        vertical_PoI.add(pos[0])

        for turn, length in instructions:
            # rotate the direction vector right/left 90 degrees
            if turn == 'R':
                dir = (dir[1], -dir[0])
            elif turn == 'L':
                dir = (-dir[1], dir[0])

            # advance `length` steps in the current direction
            pos = (pos[0] + dir[0] * length, pos[1] + dir[1] * length)

            # record the endpoint's row/column as PoI for grid mapping
            horizontal_PoI.add(pos[1])
            vertical_PoI.add(pos[0])

        horizontal_PoI, vertical_PoI = sorted(list(horizontal_PoI)), sorted(list(vertical_PoI))

        # small padding around extents (not directly used later but kept
        # for conceptual bounds)
        minX = min(vertical_PoI) - 2
        maxX = max(vertical_PoI) + 2
        minY = min(horizontal_PoI) - 2
        maxY = max(horizontal_PoI) + 2

        mapping_x = defaultdict(int)
        mapping_y = defaultdict(int)

        reverse_mapping_x = defaultdict(int)
        reverse_mapping_y = defaultdict(int)

        dungeon = defaultdict(bool)

        # Build compacted grid mapping: create a 3x3 neighborhood for each
        # intersection point so we can represent both lines and adjacent cells.
        for i in range(len(horizontal_PoI)):
            for j in range(len(vertical_PoI)):
                for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    # compacted_index -> real coordinate
                    mapping_x[3 * j + dx] = vertical_PoI[j] + dx
                    mapping_y[3 * i + dy] = horizontal_PoI[i] + dy
                    # real coordinate -> compacted_index
                    reverse_mapping_x[vertical_PoI[j] + dx] = 3 * j + dx
                    reverse_mapping_y[horizontal_PoI[i] + dy] = 3 * i + dy
                    # initialize cell as open (False = not a wall)
                    dungeon[(3 * j + dx, 3 * i + dy)] = False
        return dungeon, mapping_x, mapping_y, reverse_mapping_x, reverse_mapping_y
    
    def on_line(point, line, map_x, map_y):
        (x1, y1), (x2, y2) = line
        # convert compacted point indices back into real coordinates for test
        (px, py) = (map_x[point[0]], map_y[point[1]])

        if x1 == x2:  # Vertical line in real coordinates
            # point lies on the line if x matches and y is between endpoints
            return px == x1 and min(y1, y2) <= py <= max(y1, y2)
        elif y1 == y2:  # Horizontal line in real coordinates
            # point lies on the line if y matches and x is between endpoints
            return py == y1 and min(x1, x2) <= px <= max(x1, x2)
        else:
            assert (False), "Only horizontal or vertical lines are supported"
    
    def find_shortest_path_length(start, goal, dungeon, map_x, map_y, rev_map_x, rev_map_y):
        # map the goal real-coordinate into the compacted grid index
        goal_mapped = (rev_map_x[goal[0]], rev_map_y[goal[1]])

        # Manhattan-distance heuristic for A*
        def heuristic(cell):
            delta = (
                map_x[cell[0]] - map_x[goal_mapped[0]],
                map_y[cell[1]] - map_y[goal_mapped[1]],
            )
            return abs(delta[0]) + abs(delta[1])

        # determine bounds of compacted indices for quick OOB checks
        min_x = min([x for (x, y) in dungeon.keys()])
        max_x = max([x for (x, y) in dungeon.keys()])
        min_y = min([y for (x, y) in dungeon.keys()])
        max_y = max([y for (x, y) in dungeon.keys()])

        queue = []
        # start from the four adjacent cells around the start intersection
        start_cells = [
            (rev_map_x[start[0]] + dx, rev_map_y[start[1]] + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ]
        for cell in start_cells:
            # only consider cells that exist and are not walls
            if cell in dungeon and not dungeon[cell]:
                heapq.heappush(queue, (1 + heuristic(cell), 1, cell))
        visited = set()

        # valid goal-adjacent target cells (we must step into one of these)
        target_cells = [
            (goal_mapped[0] + dx, goal_mapped[1] + dy)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]
        ]

        # A* search loop
        while queue:
            _, cost, current = heapq.heappop(queue)

            # if current is one of the target neighbors, add final step and return
            if current in target_cells:
                cost += 1
                return cost

            if current in visited:
                continue
            visited.add(current)

            x, y = current
            # explore 4-neighbors on the compacted grid
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (x + dx, y + dy)

                out_of_bounds_check = (
                    neighbor[0] < min_x
                    or neighbor[0] > max_x
                    or neighbor[1] < min_y
                    or neighbor[1] > max_y
                )
                wall_check = neighbor in dungeon and dungeon[neighbor]

                # skip invalid / blocked positions
                if out_of_bounds_check or wall_check or neighbor not in dungeon:
                    continue

                if not dungeon[neighbor]:
                    # movement cost is Manhattan delta in real coordinates
                    delta = (
                        map_x[neighbor[0]] - map_x[current[0]],
                        map_y[neighbor[1]] - map_y[current[1]],
                    )
                    dist = abs(delta[0]) + abs(delta[1])
                    # push neighbor with priority = cost_so_far + step_cost + heuristic
                    heapq.heappush(
                        queue, (cost + dist + heuristic(neighbor), cost + dist, neighbor)
                    )
        # unreachable
        return float("inf")

    def build_dungeon(instructions):
        dungeon, map_x, map_y, rev_map_x, rev_map_y = build_intervals(instructions)

        pos = (0,0)
        dir = (0,1)
        for turn, length in instructions:
            # rotate direction according to instruction
            if turn == 'R':
                dir = (dir[1], -dir[0])
            elif turn == 'L':
                dir = (-dir[1], dir[0])

            # real segment this instruction traces from `pos` to the endpoint
            line = (pos, (pos[0] + dir[0] * length, pos[1] + dir[1] * length))

            # mark any compacted-grid cells that lie on this real segment as walls
            for (a, b) in [
                (x, y) for (x, y) in dungeon.keys() if on_line((x, y), line, map_x, map_y)
            ]:
                dungeon[(a, b)] = True

            # advance to the endpoint for the next instruction
            pos = (pos[0] + dir[0] * length, pos[1] + dir[1] * length)

        return find_shortest_path_length((0,0), pos, dungeon, map_x, map_y, rev_map_x, rev_map_y)


    # --- Part 1: return the token at (2025 mod N) ---
    if part == 1:
        result = build_dungeon(data)

    # --- Part 2: map a very large turn count into the actual integer ---
    elif part == 2:
        result = build_dungeon(data)

    # --- Part 3: same mapping but with an even larger turn count ---
    elif part == 3:
        result = build_dungeon(data)

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