from hmmlearn import hmm
import numpy as np
import pandas as pd

# Define the DNA alphabet
alphabet = ["a", "c", "g", "t"]
n_symbols = len(alphabet)  # Number of symbols in the alphabet

# Encode nucleotides as integers for hmmlearn
nucleotide_to_index = {nuc: idx for idx, nuc in enumerate(alphabet)}
index_to_nucleotide = {idx: nuc for nuc, idx in nucleotide_to_index.items()}

# Define HMM parameters
n_states = 3  # Match, Insertion, Deletion

# Adjusted Transition probabilities (real-life mutation scenarios)
trans_probs = np.array([
    [0.7, 0.2, 0.1],  # Match -> Match, Insert, Delete
    [0.3, 0.4, 0.3],  # Insert -> Match, Insert, Delete
    [0.5, 0.1, 0.4],  # Delete -> Match, Insert, Delete
])

# Adjusted Emission probabilities (mutation scenarios)
emission_probs = np.array([
    [0.25, 0.25, 0.25, 0.25],  # Match state: Equal probabilities for A, C, G, T
    [0.1, 0.4, 0.4, 0.1],      # Insert state: C and G are more likely
    [0.0, 0.0, 0.0, 0.0],      # Delete state: No emission
])

# Initial state probabilities
start_probs = np.array([0.8, 0.1, 0.1])  # Start state most likely to be "Match"

# Create the HMM model
model = hmm.MultinomialHMM(n_components=n_states, n_iter=100, tol=0.01)
model.startprob_ = start_probs
model.transmat_ = trans_probs
model.emissionprob_ = emission_probs

# Function to generate a mutated sequence using the HMM model
def generate_mutated_sequence(original_sequence):
    # Convert original sequence to integer indices
    encoded_sequence = np.array([[nucleotide_to_index[nuc]] for nuc in original_sequence])

    # Define n_trials (set to 1 since each emission corresponds to one nucleotide)
    model.n_trials = 1

    # Simulate the HMM to generate a mutated sequence
    generated_indices, _ = model.sample(len(original_sequence))

    # Convert the generated indices back to nucleotides
    generated_sequence = "".join(index_to_nucleotide[idx[0]] for idx in generated_indices)
    
    return generated_sequence

# Read the original CSV file with sequences
df = pd.read_csv('dna_sequences.csv')  # Assuming sequences are in a column named 'sequence'

# Generate mutated sequences using the HMM model
mutated_sequences = []
for seq in df['sequence1']:
    mutated_sequences.append([
        seq,  # Original sequence
        generate_mutated_sequence(seq)  # Generated mutated sequence using HMM
    ])

# Create a DataFrame with original and mutated sequences
mutated_df = pd.DataFrame(mutated_sequences, columns=["Original", "Generated"])

# Save the results to a new CSV file
mutated_df.to_csv('mutated_sequences.csv', index=False)

print("Mutated sequences saved to 'mutated_sequences.csv'.")
