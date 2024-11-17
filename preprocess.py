import os
import csv
from Bio import AlignIO, SeqIO
from itertools import combinations

# Function to clean sequences by removing non-ACGT characters (e.g., gaps or non-standard residues)
def clean_sequence(seq):
    return ''.join([base for base in seq if base in 'ACGT'])

def process_balibase_folder(folder_path, file_format="tfa", output_csv="sequence_pairs.csv"):
    """
    Process BAliBASE files in the given folder and extract sequence pairs, saving them to a CSV file.

    Args:
        folder_path (str): Path to the folder containing BAliBASE files (e.g., RV11 or RV12).
        file_format (str): Format of the files to process ('tfa' or 'msf').
        output_csv (str): Path to save the output CSV file.
    """
    sequence_pairs = []

    # Traverse through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(file_format):  # Process only specified format
            file_path = os.path.join(folder_path, file_name)
            try:
                if file_format == "tfa":
                    # For TFA format (unaligned sequences)
                    for record in SeqIO.parse(file_path, "fasta"):
                        cleaned_seq = clean_sequence(str(record.seq))
                        sequence_pairs.append({"id1": record.id, "sequence1": cleaned_seq, "id2": None, "sequence2": None})
                elif file_format == "msf":
                    # For MSF format (aligned sequences)
                    alignment = AlignIO.read(file_path, "msf")
                    # Generate pairs of sequences from the same alignment
                    for record1, record2 in combinations(alignment, 2):
                        cleaned_seq1 = clean_sequence(str(record1.seq))
                        cleaned_seq2 = clean_sequence(str(record2.seq))
                        sequence_pairs.append({
                            "id1": record1.id, "sequence1": cleaned_seq1,
                            "id2": record2.id, "sequence2": cleaned_seq2
                        })
            except Exception as e:
                print(f"Error processing {file_name}: {e}")
    
    # Save sequence pairs to CSV
    with open(output_csv, mode='w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id1', 'sequence1', 'id2', 'sequence2']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()  # Write header row
        writer.writerows(sequence_pairs)  # Write sequence pairs rows

    print(f"Sequence pairs saved to {output_csv}")

# Example Usage
if __name__ == "__main__":
    # Replace with your actual RV11 or RV12 folder path
    rv11_folder = "/Users/emerald/Desktop/uiuc_2024_fall/bioinformatic/final_proj/RV11"
    process_balibase_folder(rv11_folder, file_format="msf", output_csv="sequence_pairs.csv")
