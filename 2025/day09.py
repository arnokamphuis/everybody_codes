from collections import defaultdict
from copy import deepcopy
import sys
from time import perf_counter
from sympy import ceiling, floor, prod
from functools import cmp_to_key

# Day identifier used to locate input files for this puzzle/day
# This module is a small puzzle solution runner: it parses input files
# under `input/day{day:02d}` and runs one of three parts (1,2,3).
# Usage examples (run from the `2025` directory):
#   python day09.py 1 test   # run part 1 on the 'test' input
#   python day09.py 2 real   # run part 2 on the 'real' input

# Day identifier used to locate input files for this puzzle/day
day = 9

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
    # Each line in the input is expected to be something like "<id>:<dna>"
    # where <dna> is a sequence (string) of characters. We split on ':'
    # and build a mapping `scales` from integer id -> list(chars of dna).
    split_data = [line.split(":") for line in data]
    scales = { int(id): list(dna) for [id, dna] in split_data}

    # `pairs` groups the characters at each position across all scales.
    # Example: if scales values are ['abc','adc'], pairs becomes
    # [('a','a'), ('b','d'), ('c','c')] — one tuple per character position.
    pairs = list(zip(*(scales.values())))

    def find_possible_parents(child_id, pairs, scales):
        """Find parent candidate pairs for a given child index.

        For the child identified by `child_id` (which is an index into the
        ordered sequence of `scales` values), this function considers all
        unordered pairs of *other* scales (p1,p2). For every character
        position across the observed sequences (`pairs`), we check whether
        the child's character at that position is included in the union
        of the two candidate parents' characters at that same position.

        If for every position the child's character is covered by the union
        of the parents, then that parent pair is considered a possible
        parent combination for this child.

        Returns a list of tuples containing the parent ids (not indices).
        """
        parent_ables = []
        # enumerate over the ordered keys of scales to get index positions
        for p1_id, id1 in enumerate(scales.keys()):
            if child_id != p1_id:
                for p2_id, id2 in enumerate(scales.keys()):
                    # ensure we don't reuse the child and we only consider
                    # each unordered parent pair once (p2_id > p1_id)
                    if child_id != p2_id and p2_id > p1_id:
                        possible = True
                        # Check every character position across all samples
                        for p in pairs:
                            # characters from two parent candidates at this
                            # position; combine into a set to represent
                            # all available parent characters at this locus.
                            parents = set(p[p1_id] + p[p2_id])
                            child = set(p[child_id])
                            # Child's character(s) must be a subset of parents'
                            if not child.issubset(parents):
                                possible = False
                                break
                        if possible:
                            parent_ables.append( (id1, id2) )
        return parent_ables
    
    def calculate_similarity(dna1, dna2):
        """Calculate the similarity between two DNA sequences.

        This function zips the two DNA sequences (lists of characters) and
        returns the count of positions where the characters are equal.
        """
        return sum([c1==c2 for (c1, c2) in zip(dna1, dna2)])
    

    def find_all_relations(pairs, scales):
        """Compute possible parent relations for every scale (child).

        Returns a mapping: child_id -> list of possible (parent1, parent2)
        id tuples.
        """
        result = defaultdict(list)
        for idx, child_id in enumerate(scales.keys()):
            parent_ables = find_possible_parents(idx, pairs, scales)
            result[child_id] = parent_ables
        return result

    # Start a timer (used purely for reporting microseconds later)
    start = perf_counter()
    result = None

    # --- Part 1 ---
    if part == 1:
        # Part 1: find the unique child that has exactly one possible parent
        # pair. For that child, multiply the pairwise similarity of each
        # parent with the child across all character positions. The code
        # multiplies similarities together for the two parents and prints
        # the product as the result.
        parents = None
        child = None
        result = 1
        for idx, child_id in enumerate(scales.keys()):
            parent_ables = find_possible_parents(idx, pairs, scales)
            if len(parent_ables) == 1:
                parents = parent_ables[0]
                for p in parents:
                    result *= calculate_similarity(scales[p], scales[child_id])
        
    # --- Part 2 ---
    elif part == 2:
        # Part 2: similar to part 1, but sum the parent-product similarity
        # for every child that has exactly one parent pair.
        result = 0
        for idx, child_id in enumerate(scales.keys()):
            similarity = 1
            parent_ables = find_possible_parents(idx, pairs, scales)
            if len(parent_ables) == 1:
                parents = parent_ables[0]
                for p in parents:
                    similarity *= calculate_similarity(scales[p], scales[child_id])
                result += similarity
    # --- Part 3 ---
    elif part == 3:

        # Part 3: Build connected "families" of scales based on the
        # parent relations. Two scales belong to the same family if there is
        # any parent-child link connecting them (directly or indirectly).
        # We perform a depth-first traversal (build_family) to collect a
        # family's members starting from a scale, then repeatedly merge any
        # overlapping families until no merges remain. Finally, the result
        # is the sum of ids in the largest family (by size).

        def build_family(child_id, relations, scales, family):
            # Recursively add the child and any parents referenced by its
            # relations to the family set. `relations` maps child_id -> list
            # of (parent1_id, parent2_id) tuples.
            family.add(child_id)
            for other_id in relations[child_id]:
                if other_id[0] not in family:
                    build_family(other_id[0], relations, scales, family)
                if other_id[1] not in family:
                    build_family(other_id[1], relations, scales, family)

        relations = find_all_relations(pairs, scales)
        families = []
        remaining = set(scales.keys())
        # Extract connected components via DFS
        while remaining:
            child_id = remaining.pop()
            fam = set()
            build_family(child_id, relations, scales, fam)
            families.append(fam)
            remaining = remaining - fam

        # Merge any overlapping families until stable (safety: this
        # consolidates any partial overlap that DFS might have separated)
        while True:
            merged = False
            for i in range(len(families)):
                for j in range(i+1, len(families)):
                    if families[i].intersection(families[j]):
                        families[i] = families[i].union(families[j])
                        families.pop(j)
                        merged = True
                        break
                if merged:
                    break
            if not merged:
                break

        # The final result is the sum of ids in the largest family
        largest_family = max(families, key=lambda f: len(f))
        result = sum(largest_family)
        
    # Stop timing and print result with microsecond precision (rounded up)
    end = perf_counter()

    # Print the result and elapsed time in microseconds (rounded up).
    print(f"Part {part} ({ceiling((end - start) * 1000000)} micros): \t{result}")


if part == 0:
    # When `part` is 0 run all parts in sequence
    run(1, sort)
    run(2, sort)
    run(3, sort)
else:
    run(part, sort)