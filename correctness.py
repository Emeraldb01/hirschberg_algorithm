import pandas as pd

def verify_alignments(hir_file, glo_file):
    """
    Compares the sequence alignments between Hirschberg and Global Alignment methods.
    
    Parameters:
        hir_file (str): Path to the Hirschberg results CSV file.
        glo_file (str): Path to the Global Alignment results CSV file.
    
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

    # Compare sequences and flag mismatches
    mismatches = []
    for idx, (hir_seq, glo_seq) in enumerate(zip(hir_df['Sequences'], glo_df['Sequences'])):
        if hir_seq != glo_seq:
            mismatches.append(idx + 1)  # Use 1-based indexing for clarity

    # Output results
    if mismatches:
        print(f"Alignment mismatch found in {len(mismatches)} cases.")
        print(f"Mismatched alignment indices: {mismatches}")
    else:
        print("All alignments match. The second method is consistent with the first.")

# Example usage
verify_alignments('results/hir_mut_results.csv', 'results/glo_mut_results.csv')
