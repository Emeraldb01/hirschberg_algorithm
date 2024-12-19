import pandas as pd

def calculate_alignment_score(seq1, seq2, delta):
    """
    Calculate the alignment score between two sequences using the given delta function.
    """
    score = 0
    # Ensure the sequences are of equal length by aligning with gaps
    max_len = max(len(seq1), len(seq2))
    seq1 = seq1.ljust(max_len, '-')
    seq2 = seq2.ljust(max_len, '-')

    # Calculate score by iterating through aligned sequences
    for s1, s2 in zip(seq1, seq2):
        score += delta[s1][s2]
    
    return score

def verify_alignments(hir_file, glo_file, delta):
    """
    Compares the alignment scores between Hirschberg and Global Alignment methods.
    
    Parameters:
        hir_file (str): Path to the Hirschberg results CSV file.
        glo_file (str): Path to the Global Alignment results CSV file.
        delta (dict): The scoring matrix (delta) used for calculating the alignment scores.
    
    Returns:
        None
    """
    # Load both CSV files
    hir_df = pd.read_csv(hir_file)
    glo_df = pd.read_csv(glo_file)
    
    # Ensure both dataframes have the same number of rows
    if len(hir_df) != len(glo_df):
        print("The number of alignments in the two files differs. Cannot compare.")
        return

    # Compare alignment scores and flag mismatches
    mismatches = []
    for idx, (hir_seq, glo_seq) in enumerate(zip(hir_df['Sequences'], glo_df['Sequences'])):
        # Calculate alignment scores for both Hirschberg and Global methods
        hir_score = calculate_alignment_score(hir_seq.split()[0], hir_seq.split()[1], delta)  # Split sequence if necessary
        glo_score = calculate_alignment_score(glo_seq.split()[0], glo_seq.split()[1], delta)  # Split sequence if necessary

        # Compare the scores
        if hir_score != glo_score:
            mismatches.append(idx + 1)  # Use 1-based indexing for clarity

    # Output results
    if mismatches:
        print(f"Alignment score mismatch found in {len(mismatches)} cases.")
        print(f"Mismatched alignment indices: {mismatches}")
    else:
        print("All alignment scores match. The second method is consistent with the first.")

# Example usage
keys = ['A', 'C', 'T', 'G', '-']
delta = {}

# Generate the delta matrix with gap scoring as 0 for matching gaps
for i in range(len(keys)):
    delta[keys[i]] = {
        k: (0 if keys[i] == '-' and k == '-' else (1 if keys[i] == k else -1))
        for k in keys
    }

# Example file paths
hir_file = 'alignment_results_global.csv'
glo_file = 'alignment_results_hirschberg.csv'

verify_alignments(hir_file, glo_file, delta)
