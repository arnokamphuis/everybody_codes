from collections import defaultdict
from copy import deepcopy
from filecmp import cmp
import functools
import sys
from time import perf_counter
from grapheme import length
from sympy import ceiling, floor, prod

# Day identifier used to locate input files for this puzzle/day
day = 10

# The script expects two CLI args: the part number and which input set to use
# Example usage: `python day08.py 1 test`  or `python day08.py 2 real`
if len(sys.argv) != 3:
    print("invalid command")
    exit()
# `part` chooses which puzzle/algorithm to run (1, 2 or 3 for this file)
part = int(sys.argv[1])
# `sort` chooses which input file variant to use (usually 'test' or 'real')
sort = sys.argv[2]


def run(part, sort):
    """Run the chosen part of the puzzle using the selected input file.

    The input files are expected to live under `input/day{day:02d}` and be
    named like `p{part}-test.txt` or `p{part}-real.txt`.
    """
    filename = 'input/day{0:02d}/p{1}-{2}.txt'.format(day, part, sort)
    # Read and strip all lines from the input file
    with open(filename, 'r') as file:
        data = [line.strip() for line in file]

    # Build a 2D grid representation (list of lists of chars) and derive
    # dimensions. The puzzle uses a grid with symbols:
    #   'D' = dragon, 'S' = sheep, '#' = hideout, other chars allowed.
    grid = [list(d) for d in data]
    R = len(grid)
    C = len(grid[0])

    # Create sets of coordinates for quick membership tests. Using sets
    # makes it easy to compute intersections (e.g., sheep eaten by dragons)
    dragon = set([(r,c) for r in range(R) for c in range(C) if grid[r][c]=='D'])
    sheep = set([(r,c) for r in range(R) for c in range(C) if grid[r][c]=='S'])
    hideouts = set([(r,c) for r in range(R) for c in range(C) if grid[r][c]=='#'])

    # Start a timer (used purely for reporting microseconds later)
    start = perf_counter()
    result = None

    def reachable_in_1_move(from_positions):
        """Return set of board coordinates reachable in one knight-like move.

        The movement pattern used here matches chess knight moves: two in
        one direction and one in the other. This helper takes an iterable
        of coordinate tuples and returns the set of valid coordinates that
        lie within the grid bounds.
        """
        moves = [(-2,1), (-2,-1), (2, 1), (2,-1), (1,2), (1,-2), (-1,2), (-1,-2)]
        possible = set([(r+dr, c+dc) for (r,c) in from_positions for (dr,dc) in moves])
        # Filter out-of-bounds positions
        possible = set([(r,c) for (r,c) in possible if 0 <= r < R and 0 <= c < C])
        return possible
    
    def update_sheep(sheep):
        """Move each sheep one row down if possible.

        Sheep move downward (increase row index). If a sheep is on the
        bottom row it cannot move further and is dropped (represented by
        filtering `None` results). The function returns a new set of
        coordinates for sheep after the move.
        """
        return set([(r+1,c) if r+1 < R else None for (r,c) in sheep]) - set([None])

    @functools.cache
    def count_different_moves(sheep, dragon, turn='S'):
        """Count distinct move sequences from the current state.

        This recursive function counts the number of different game-tree
        paths reachable from the current configuration of `sheep` (a tuple
        or iterable of coordinates) and the `dragon` coordinate. The
        `turn` argument alternates between 'S' (sheep) and 'D' (dragon).

        Notes on representation and behavior:
        - The function is cached to avoid recomputing identical states.
        - `sheep` is expected to be an ordered tuple when recursion uses
          sequence operations; ordering is used only as a stable state
          representation for caching.
        - On the sheep's turn ('S'), each sheep either moves down one row
          or is considered blocked if at the bottom. Sheep movement that
          would land on the dragon is only allowed if that landing cell
          is a hideout (safe for sheep).
        - On the dragon's turn ('D'), the dragon can move to any
          reachable knight-position. If the dragon moves onto a sheep's
          coordinate and that coordinate is not a hideout, that sheep is
          removed for subsequent recursion.

        The function returns the count of distinct move sequences from the
        current state until termination conditions are reached.
        """
        if turn == 'S':
            if len(sheep) == 0: return 1
            total = 0
            move_count = 0
            for idx, s in enumerate(sheep):
                # If sheep is on the bottom row it cannot move further
                if s[0]+1 >= R:
                    move_count += 1
                # Otherwise, sheep moves down unless the dragon is there
                # and it's not a hideout. If the move is allowed, recurse
                # with the updated sheep tuple and switch turn to dragon.
                elif dragon != (s[0]+1, s[1]) or (s[0]+1, s[1]) in hideouts:
                    move_count += 1
                    total += count_different_moves((*sheep[:idx], (s[0]+1, s[1]), *sheep[idx+1:]), dragon, 'D')
            # If no sheep could move (move_count == 0), the turn passes to dragon
            if move_count == 0: return count_different_moves(sheep, dragon, 'D')
            return total
        if turn == 'D':
            total = 0
            # Consider every knight-like move the dragon can make this turn
            for nd in reachable_in_1_move({dragon}):
                # Remove any sheep that are eaten (dragon moved onto them)
                # unless the square is a hideout — then sheep survive.
                total += count_different_moves(tuple((s for s in sheep if s != nd or nd in hideouts)), nd, 'S')
            return total

    # --- Part 1 ---
    if part == 1:
        # Part 1: Determine how many distinct sheep positions the dragon
        # can reach within a small number of knight-like moves. This part
        # iteratively grows the set of reachable dragon positions and
        # accumulates sheep positions that coincide with those reachable
        # cells.
        reachable = dragon
        sheep_reachable = set()
        for _ in range(3 if sort=='test' else 4):
            moves = reachable_in_1_move(reachable)
            reachable = moves
            sheep_reachable |= (set(sheep) & moves)

        result = len(sheep_reachable)

    # --- Part 2 ---
    elif part == 2:
        # Part 2: Simulate multiple rounds. Each round the dragon moves to
        # all reachable positions (treated as the set of dragon positions),
        # eats any sheep not in hideouts, then sheep move down, and some
        # may be eaten again. The total number of sheep eaten across all
        # rounds is accumulated.
        all_sheep_eaten = 0
        rounds = 3 if sort=='test' else 20
        for r in range(rounds):
            dragon = reachable_in_1_move(dragon)
            sheep_eaten = dragon & (sheep - hideouts)
            all_sheep_eaten += len(sheep_eaten)
            # Sheep that survived (not eaten) move down
            sheep = update_sheep(sheep - sheep_eaten)
            # After moving, sheep can again be in dragon positions
            sheep_eaten = dragon & (sheep - hideouts)
            all_sheep_eaten += len(sheep_eaten)
            sheep = sheep - sheep_eaten
        result = all_sheep_eaten
    # --- Part 3 ---
    elif part == 3:
        # Part 3: Count all distinct move sequences from the starting state.
        # Convert `sheep` to a tuple (deterministic ordering) and use a single
        # dragon coordinate. `count_different_moves` is cached to avoid
        # recomputation over identical states.
        result = count_different_moves(tuple(sheep), dragon.pop(), 'S')
    
    # Stop timing and print result with microsecond precision (rounded up)
    end = perf_counter()

    # Print the result and elapsed time in microseconds (rounded up).
    print(f"Part {part}: ({int(ceiling((end - start) * 1000000)):>12} microseconds): \t{result}")


if part == 0:
    # When `part` is 0 run all parts in sequence
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)