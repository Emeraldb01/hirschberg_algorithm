import csv

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

def process_csv(input_csv, output_csv, delta):
    """
    Process the CSV file to calculate alignment scores and add them as a new column.
    """
    try:
        with open(input_csv, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            fieldnames = reader.fieldnames + ['Alignment Score']  # Add new column for the score

            # Read the rows and calculate the alignment score
            rows = []
            for row in reader:
                seq1, seq2 = row['Sequences'].split()  # Assuming sequences are separated by a comma
                score = calculate_alignment_score(seq1, seq2, delta)
                row['Alignment Score'] = score
                rows.append(row)

        # Write the updated rows to a new CSV file
        with open(output_csv, mode='w', newline='') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        
        print(f"New file saved successfully to: {output_csv}")
    
    except FileNotFoundError:
        print(f"Error: The input file '{input_csv}' was not found.")
    except Exception as e:
        print(f"Error occurred: {e}")

# Example usage
keys = ['A', 'C', 'T', 'G', '-']
delta = {}

# Generate the delta matrix with gap scoring as 0 for matching gaps
for i in range(len(keys)):
    delta[keys[i]] = {
        k: (0 if keys[i] == '-' and k == '-' else (1 if keys[i] == k else -1))
        for k in keys
    }

# Call the function with your input CSV and output CSV paths
input_csv = 'alignment_results_hirschberg.csv'  # Path to the input CSV
output_csv = 'alignment_results_hirschberg.csv'  # Path for the output CSV

process_csv(input_csv, output_csv, delta)
