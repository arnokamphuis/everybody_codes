"""
Day 1, 2025 Part III: Enigmatus Modular Puzzle Solution (Sum of Remainders)

Implements the sum-of-remainders 'eni' function variant as described in the story.
"""

def eni_sum_remainders(N, EXP, MOD):
    """
    Efficiently computes the sum of all remainders produced during modular exponentiation:
    - N: base number
    - EXP: exponent (number of multiplications)
    - MOD: modulus
    Returns: integer sum of all remainders encountered in the sequence.
    """
    if EXP == 0:
        return 0
    score = 1
    total = 0
    seen = dict()  # (score) -> (step, total)
    steps = 0
    while steps < EXP:
        score = (score * N) % MOD
        total += score
        key = score
        if key in seen:
            # Cycle detected
            prev_step, prev_total = seen[key]
            cycle_len = steps - prev_step
            cycle_sum = total - prev_total
            remaining_steps = EXP - steps - 1
            if cycle_len > 0:
                skip_cycles = remaining_steps // cycle_len
                total += skip_cycles * cycle_sum
                steps += skip_cycles * cycle_len
        else:
            seen[key] = (steps, total)
        steps += 1
    return total

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

def compute_highest_sum_remainders(input_path):
    """
    Efficiently computes the highest sum of remainders for all parameter sets in the input file using eni_sum_remainders.
    """
    max_sum = 0
    with open(input_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            A, B, C, X, Y, Z, M = parse_line(line)
            result = (
                eni_sum_remainders(A, X, M) +
                eni_sum_remainders(B, Y, M) +
                eni_sum_remainders(C, Z, M)
            )
            if result > max_sum:
                max_sum = result
    return max_sum

if __name__ == "__main__":
    # Example: sum of remainders for N=2, EXP=7, MOD=5
    print("eni_sum_remainders(2, 7, 5) =", eni_sum_remainders(2, 7, 5))
    # Example input path (update as needed)
    input_path = r"c:/Users/ik/git/everybody_codes/stories/echoes_of_enigmatus/day01_2025/input/everybody_codes_e1_q01_p3.txt"
    highest = compute_highest_sum_remainders(input_path)
    print("Highest result:", highest)
