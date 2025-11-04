"""
Day 1, 2025 Part II: Enigmatus Modular Puzzle Solution (Truncated)

Implements the truncated 'eni' function (last 5 remainders) and supporting logic as described in the story.
"""

def eni_truncated(N, EXP, MOD, k=5):
    """
    Efficiently computes the truncated 'eni' function (last k remainders) for large EXP using cycle detection.
    - N: base number
    - EXP: exponent (number of multiplications)
    - MOD: modulus
    - k: number of last remainders to keep (default 5)
    Returns: integer formed by joining the last k remainders as described.
    """
    if EXP == 0:
        return 0
    score = 1
    remainders = []
    seen = dict()  # (score) -> (step, copy of remainders)
    steps = 0
    while steps < EXP:
        score = (score * N) % MOD
        remainders.insert(0, str(score))
        if len(remainders) > k:
            remainders.pop()
        key = (score, tuple(remainders))
        if key in seen:
            # Cycle detected
            prev_step = seen[key]
            cycle_len = steps - prev_step
            remaining_steps = EXP - steps - 1
            if cycle_len > 0:
                skip_cycles = remaining_steps // cycle_len
                steps += skip_cycles * cycle_len
        else:
            seen[key] = steps
        steps += 1
    return int(''.join(remainders)) if remainders else 0

def parse_line(line):
    parts = line.strip().split()
    values = {}
    for part in parts:
        key, val = part.split('=')
        values[key] = int(val)
    return values['A'], values['B'], values['C'], values['X'], values['Y'], values['Z'], values['M']

def compute_highest_sum_truncated(input_path, k=5):
    """
    Efficiently computes the highest sum for all parameter sets in the input file using the optimized eni_truncated.
    """
    max_sum = 0
    with open(input_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            A, B, C, X, Y, Z, M = parse_line(line)
            result = (
                eni_truncated(A, X, M, k) +
                eni_truncated(B, Y, M, k) +
                eni_truncated(C, Z, M, k)
            )
            if result > max_sum:
                max_sum = result
    return max_sum

if __name__ == "__main__":
    # Example from the story: eni_truncated(2, 7, 5) should return 34213
    print("eni_truncated(2, 7, 5) =", eni_truncated(2, 7, 5))
    # Example input path (update as needed)
    input_path = r"c:/Users/ik/git/everybody_codes/stories/echoes_of_enigmatus/day01_2025/input/everybody_codes_e1_q01_p2.txt"
    highest = compute_highest_sum_truncated(input_path)
    print("Highest result:", highest)
