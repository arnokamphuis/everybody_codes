from collections import deque
import sys
from time import perf_counter
from sympy import ceiling


# Day identifier used to locate input files for this puzzle/day
day = 12


# The script expects exactly two CLI args: the part number and which input set
# to use. Typical usage examples:
#   python day12.py 1 test    # run part 1 on the 'test' input
#   python day12.py 2 real    # run part 2 on the 'real' input
if len(sys.argv) != 3:
    print("invalid command")
    exit()

# `part` chooses which puzzle/algorithm to run (1, 2 or 3 for this file)
part = int(sys.argv[1])
# `sort` chooses which input file variant to use (usually 'test' or 'real')
sort = sys.argv[2]


def run(part, sort):
    """Execute the selected part using the input variant specified by `sort`.

    The function reads the input file located at `input/day{day:02d}/p{part}-{sort}.txt`.
    It then parses the input into a 2D integer grid and runs one of three
    behaviors depending on `part`:
      - part 1: compute size reachable from the top-left (0,0)
      - part 2: compute union of reachable from top-left and bottom-right
      - part 3: repeatedly pick the largest reachable area (3 times),
                making already-counted cells inaccessible between picks.

    Important: This function only adds comments and does not change the
    original algorithms or behavior.
    """

    # Build the input filename and read lines, stripping trailing newline
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    # Convert each input line of digits into a list of integers forming the grid.
    # Example: '123' -> [1, 2, 3]
    grid = [list(map(int, list(line))) for line in data]
    height = len(grid)
    width = len(grid[0])


    def floodfill_queue(x, y, g):
        """Breadth-first flood fill (BFS) from starting coordinate (x, y).

        Behavior and invariants:
        - Uses a queue (FIFO) so regions are explored breadth-first.
        - `seen` records visited cells so we never process the same cell
          more than once (avoids infinite loops and duplicate counting).
        - Movement is allowed only in the four cardinal directions (N,S,E,W).
        - A neighbor cell `(nx, ny)` is enqueued only if:
            * it lies within the grid bounds,
            * its value is not -1 (value -1 is treated as blocked/inaccessible),
            * its numeric value `g[ny][nx]` is less than or equal to the
              current cell's value `g[cy][cx]`.

        The last condition (g[ny][nx] <= g[cy][cx]) means the flood only
        flows to equal-or-lower valued neighbors, which matches many puzzles
        where values represent heights or thresholds.

        The function returns the `seen` set containing all reachable
        coordinates (x,y) from the start under these rules.
        """

        queue = deque()
        queue.append((x, y))
        seen = set()

        # Standard BFS loop
        while queue:
            cx, cy = queue.popleft()

            # Skip if already visited
            if (cx, cy) in seen:
                continue
            seen.add((cx, cy))

            # Explore four neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = cx + dx, cy + dy

                # Check bounds and that the neighbor isn't marked blocked (-1)
                if 0 <= nx < width and 0 <= ny < height and g[ny][nx] != -1:
                    # Only allow movement to neighbors with value <= current
                    # This enforces a monotonic non-increasing constraint
                    if g[ny][nx] <= g[cy][cx]:
                        queue.append((nx, ny))

        return seen


    def find_max(g):
        """Exhaustively try every grid coordinate as a BFS start and return
        the coordinate which yields the largest reachable set.

        This helper is used to choose the best starting point when we want
        the single largest connected (by the flood rules) region in `g`.
        It returns the position `(x, y)` that produced the largest `seen` set.
        """

        max_val = -1
        max_pos = (-1, -1)

        # Try every possible starting cell; this is O(width*height*BFS).
        # For small grids this is acceptable; for large inputs it would be
        # expensive and would need optimization.
        for y in range(height):
            for x in range(width):
                seen = floodfill_queue(x, y, g)
                if max_val < len(seen):
                    max_val = len(seen)
                    max_pos = (x, y)
        return max_pos


    # Start a timer to measure elapsed time for this run (reported in microseconds)
    start = perf_counter()
    result = None

    # --- Part 1: size of region reachable from top-left (0,0) ---
    if part == 1:
        # compute the number of coordinates reachable from (0, 0)
        result = len(floodfill_queue(0, 0, grid))

    # --- Part 2: union of two regions (top-left and bottom-right) ---
    elif part == 2:
        # compute reachable from (0,0) and from (width-1, height-1) and take union
        a = floodfill_queue(0, 0, grid)
        b = floodfill_queue(width - 1, height - 1, grid)
        result = len(a | b)

    # --- Part 3: choose the three largest disjoint regions ---
    elif part == 3:
        # We'll collect coordinates that have already been counted in `total_seen`.
        # Between each selection of the largest region we mark those coordinates
        # as blocked (-1) in a temporary copy so subsequent `find_max` calls do
        # not re-select the same cells. This yields three disjoint areas.
        total_seen = set()
        for _ in range(3):
            # Build a temporary grid where already-counted coordinates are
            # replaced by -1 (blocked). We leave other cells unchanged.
            newgrid = [[-1 if (c, r) in total_seen else ng for c, ng in enumerate(row)]
                       for r, row in enumerate(grid)]

            # Choose the best starting point on the modified grid
            x, y = find_max(newgrid)
            # Get its reachable set and add those coordinates to the running set
            seen = floodfill_queue(x, y, newgrid)
            total_seen |= seen

        # The final answer is the count of unique coordinates covered by the
        # three selected regions.
        result = len(total_seen)

    # Stop timing and print result with microsecond precision (rounded up)
    end = perf_counter()
    print(f"Part {part}: ({int(ceiling((end - start) * 1000000)):>12} microseconds): \t{result}")


if part == 0:
    # When `part` is 0 run all parts in sequence for convenience
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)