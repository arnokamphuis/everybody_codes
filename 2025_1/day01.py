"""
Day 1, 2025: Enigmatus Modular Puzzle Solution

Implements the 'eni' function and supporting logic as described in the story.
"""

def eni(N, EXP, MOD):
    """
    Implements the 'eni' function:
    - Starts with score = 1.
    - Repeats EXP times:
        - Multiplies score by N.
        - Takes score modulo MOD.
        - Prepends the remainder to a list.
    - Joins the list of remainders into a single integer.
    """
    score = 1
    remainders = []
    for _ in range(EXP):
        score = (score * N) % MOD
        remainders.insert(0, str(score))  # Insert at the start (reverse order)
    return int(''.join(remainders))

def parse_line(line):
    """
    Parses a line like 'A=2 B=8 C=5 X=7 Y=4 Z=5 M=20'
    Returns: tuple (A, B, C, X, Y, Z, M)
    """
    parts = line.strip().split()
    values = {}
    for part in parts:
        key, val = part.split('=')
        values[key] = int(val)
    return values['A'], values['B'], values['C'], values['X'], values['Y'], values['Z'], values['M']

def compute_highest_sum(input_path):
    """
    Reads the input file, computes the sum for each parameter set,
    and returns the highest sum found.
    """
    max_sum = 0
    with open(input_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue  # Skip empty lines
            A, B, C, X, Y, Z, M = parse_line(line)
            result = eni(A, X, M) + eni(B, Y, M) + eni(C, Z, M)
            if result > max_sum:
                max_sum = result
    return max_sum

# Example usage and test
if __name__ == "__main__":
    # Example from the story: eni(2, 4, 5) should return 1342
    print("eni(2, 4, 5) =", eni(2, 4, 5))
    # Example input path (update as needed)
    input_path = r"c:/Users/ik/git/everybody_codes/stories/echoes_of_enigmatus/day01_2025/input/everybody_codes_e1_q01_p1.txt"
    highest = compute_highest_sum(input_path)
    print("Highest result:", highest)
