from collections import defaultdict, deque
import sys
from time import perf_counter
from sympy import ceiling


# Day identifier used to locate input files for this puzzle/day
day = 18

# Module overview:
#
# This script parses a textual description of a tree-like "plant" network
# from the day's input. The input contains one or more plant descriptions
# (blocks separated by empty lines) followed optionally by a list of numeric
# input `patterns`. Each plant node can have parent nodes (inputs) and
# branches to child nodes, with integer "thickness" values that scale
# contributions. The goal is to compute the total energy reaching an
# end node given various input assignments (parts 1-3).
#
# Key data structures:
# - `plants`: dict mapping plant_id -> {'thickness': int, 'branches': {child:thick}, 'parents': {parent:thick}}
# - `patterns`: list of input vectors used by parts 2 and 3
# - `end_node_id`: id of the unique leaf node (no outgoing branches)
#
# The main recursive routine is `total_energy(plant_id, inputs)` which
# computes how much energy flows to `plant_id` given input values.

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

    # `patterns` optionally holds several input vectors that appear after a
    # double-empty-line separator in the file. We detect a double-empty pair
    # and split the input into the plant description section and the patterns
    # section. Each pattern is a whitespace-separated line of integers.
    patterns = []
    double_empty = [idx for idx, line in enumerate(zip(data, data[1:])) if line[0] == '' and line[1] == '']
    if double_empty:
        patterns = [list(map(int, line.split())) for line in data[double_empty[0] + 2 :]]
        # truncate `data` to only the plant-description part
        data = data[: double_empty[0] + 1]

    # compute indices that separate plant description blocks (empty lines)
    empty_line_idxs = [0] + [i + 1 for i, line in enumerate(data) if line == ''] + (
        [len(data) + 1] if patterns == [] else []
    )

    # `plants` maps plant id -> node info. We use defaultdict(dict) initially
    # and ensure an entry exists for the special `None` input node.
    plants = defaultdict(dict)
    plants[None] = {'thickness': 0, 'branches': {}, 'parents': {}}

    # Each contiguous block in `data` describes one plant node. Parse those
    # blocks into `plants[plant_id]` entries. Block header contains the id
    # and thickness; following lines describe either a branch link to another
    # plant or an input (parent) with a thickness.
    for i, j in zip(empty_line_idxs, empty_line_idxs[1:]):
        block = data[i : j - 1]
        # Header format example: "Plant 3 thickness=4:" (parser is positional)
        plant_id = int(block[0].split()[1])
        plant_thickness = int(block[0].split()[4][:-1])

        plants[plant_id] = {
            'thickness': plant_thickness,
            'branches': defaultdict(int),
            'parents': defaultdict(int),
        }

        # Parse body lines describing parents/branches
        for line in block[1:]:
            parts = line.split()
            if parts[1] == 'branch':
                # branch line example: "  branch to 5 thickness 2"
                target = int(parts[4])
                thickness = int(parts[7])
                # record that this plant has a parent link to `target`
                plants[plant_id]['parents'][target] = thickness
            else:
                # input line example: "  input value 3"
                plants[plant_id]['parents'][None] = int(parts[5])

    # Convert parent pointers into child `branches` lists. For every parent
    # declared in a plant's `parents` map, add this plant as a child on the
    # parent's `branches` mapping. This builds the directed graph edges.
    for pid, plant in plants.items():
        parents = plant['parents']
        for parent_target, parent_thickness in parents.items():
            plants[parent_target]['branches'][pid] = parent_thickness

    # Identify the unique end node (leaf) which has no outgoing branches.
    end_node_id = [pid for pid, p in plants.items() if len(p['branches']) == 0][0]

    def total_energy(plant_id, inputs):
        # Recursive computation of total energy arriving at `plant_id`.
        # - `inputs` is a dict mapping input node ids -> supplied value (int/0/1)
        # - If the node has a direct `None` parent, it is an input node and
        #   returns thickness * inputs[plant_id].
        # - Otherwise, sum contributions from each parent scaled by the
        #   parent's thickness, and if the total is less than this node's
        #   thickness the node contributes 0 (insufficient input).
        thickness = plants[plant_id]['thickness']
        parents = plants[plant_id]['parents']

        # base case: direct input is provided
        if None in parents:
            return thickness * inputs[plant_id]

        # recursive accumulation from parent nodes
        total = 0
        for parent_id, parent_thickness in parents.items():
            total += parent_thickness * total_energy(parent_id, inputs)

        # threshold check: if upstream total is less than node thickness,
        # the node fails and yields zero; otherwise it passes the total
        if total < thickness:
            return 0

        return total

    # Start a timer to measure elapsed time for this run (reported in microseconds)
    start = perf_counter()
    result = None

    # --- Part 1: 
    if part == 1:
        # Part 1: assume every input node supplies value 1 and compute the
        # total energy reaching the end node under that uniform input.
        inputs = {pid: 1 for pid, plant in plants.items() if None in plant['parents']}
        result = total_energy(end_node_id, inputs)

    # --- Part 2: 
    elif part == 2:
        # Part 2: for each provided pattern (a list of input values), map
        # it to the input node ids (starting at 1) and accumulate the
        # energy reaching the end node.
        result = 0
        for pattern in patterns:
            inputs = {pid: val for pid, val in enumerate(pattern, start=1)}
            result += total_energy(end_node_id, inputs)

    # --- Part 3: 
    elif part == 3:
        # Part 3: compute a maximal possible input vector `max_input` where
        # an input node is set to 1 only if all its immediate children would
        # receive positive thickness (heuristic derived from puzzle).
        max_input = defaultdict(bool)
        input_nodes = [pid for pid, plant in plants.items() if None in plants[pid]['parents']]
        for inp in input_nodes:
            # find nodes that consume `inp` as a parent
            second_layer = [pid for pid, plant in plants.items() if inp in plants[pid]['parents']]
            # thickness values from `inp` into those second-layer nodes
            thickness_second_layer = [plants[inp]['branches'][pid] for pid in second_layer]
            # set to 1 only if all out-going thicknesses are positive
            max_input[inp] = int(all(thick > 0 for thick in thickness_second_layer))

        # compute the maximum energy achievable with `max_input` assignment
        max_energy = total_energy(end_node_id, max_input)

        # for each provided pattern, if it yields positive energy, add the
        # difference (max_energy - pattern_energy) to the result
        result = 0
        for pattern in patterns:
            inputs = {pid: val for pid, val in enumerate(pattern, start=1)}
            te = total_energy(end_node_id, inputs)
            if te > 0:
                result += max_energy - te

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