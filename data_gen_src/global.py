import pandas as pd
import time
import tracemalloc
import sys
from memory_profiler import profile
from io import StringIO

# Constants for traceback directions
UP = (-1, 0)
LEFT = (0, -1)
TOPLEFT = (-1, -1)
ORIGIN = (0, 0)

def traceback_global(v, w, pointers):
    """
    Perform traceback to recover alignment from the pointers matrix.

    :param v: First sequence
    :param w: Second sequence
    :param pointers: Pointer matrix indicating traceback directions
    :return: Aligned sequences as a string
    """
    i, j = len(v), len(w)
    new_v, new_w = [], []
    while True:
        di, dj = pointers[i][j]
        if (di, dj) == LEFT:
            new_v.append('-')
            new_w.append(w[j - 1])
        elif (di, dj) == UP:
            new_v.append(v[i - 1])
            new_w.append('-')
        elif (di, dj) == TOPLEFT:
            new_v.append(v[i - 1])
            new_w.append(w[j - 1])
        i, j = i + di, j + dj
        if i <= 0 and j <= 0:
            break
    return ''.join(new_v[::-1]) + '\n' + ''.join(new_w[::-1])


@profile
def global_align(v, w, delta):
    """
    Perform global alignment using dynamic programming.

    :param v: First sequence
    :param w: Second sequence
    :param delta: Scoring matrix
    :return: Alignment, score, elapsed time, and memory usage
    """
    start_time = time.time()
    tracemalloc.start()

    M = [[0 for _ in range(len(w) + 1)] for _ in range(len(v) + 1)]
    pointers = [[ORIGIN for _ in range(len(w) + 1)] for _ in range(len(v) + 1)]

    # Initialize the first column and row
    for i in range(1, len(v) + 1):
        cur_v = v[i - 1]
        M[i][0] = M[i - 1][0] + delta[cur_v]["-"]
        pointers[i][0] = UP

    for j in range(1, len(w) + 1):
        cur_w = w[j - 1]
        M[0][j] = M[0][j - 1] + delta["-"][cur_w]
        pointers[0][j] = LEFT

    # Fill in the DP matrix
    for i in range(1, len(v) + 1):
        for j in range(1, len(w) + 1):
            cur_v = v[i - 1]
            cur_w = w[j - 1]

            left_score = M[i][j - 1] + delta["-"][cur_w]
            top_score = M[i - 1][j] + delta[cur_v]["-"]
            diagonal_score = M[i - 1][j - 1] + delta[cur_v][cur_w]

            M[i][j] = max(left_score, diagonal_score, top_score)

            if M[i][j] == left_score:
                pointers[i][j] = LEFT
            elif M[i][j] == top_score:
                pointers[i][j] = UP
            else:
                pointers[i][j] = TOPLEFT

    score = M[len(v)][len(w)]
    alignment = traceback_global(v, w, pointers)

    # Stop memory tracking and calculate time elapsed
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    elapsed_time = end_time - start_time

    print(f"Time taken: {elapsed_time:.4f} seconds")
    print(f"Current memory usage: {current / 10 ** 6:.2f} MB")
    print(f"Peak memory usage: {peak / 10 ** 6:.2f} MB")

    return alignment, score


def test_alignment(csv_file, delta, alignment_model):
    """
    Test an alignment model on a CSV file of sequences.

    :param csv_file: Path to the CSV file containing sequences.
    :param delta: Scoring matrix for alignment.
    :param alignment_model: The alignment function to test.
    """
    df = pd.read_csv(csv_file)
    for idx, row in df.iterrows():
        seq1, seq2 = row['sequence1'], row['sequence2']
        print(f"\n=== Alignment {idx + 1}: {seq1[:10]}... vs {seq2[:10]}... ===")
        aligned_seq, score = alignment_model(seq1, seq2, delta)
        print(f"Alignment:\n{aligned_seq}")
        print(f"Score: {score}")


if __name__ == "__main__":
    import argparse

    # Scoring matrix initialization
    keys = ['A', 'C', 'T', 'G', '-']
    delta = {
        key: {k: 1 if key == k else -1 for k in keys} for key in keys
    }

    # Argument parser
    parser = argparse.ArgumentParser(description="Global Alignment with Memory Profiling")
    parser.add_argument("csv_file", help="Path to the CSV file containing sequences.")
    args = parser.parse_args()

    # Run alignment test
    test_alignment(csv_file=args.csv_file, delta=delta, alignment_model=global_align)
