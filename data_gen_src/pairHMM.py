from hmmlearn import hmm
import numpy as np
import pandas as pd
import random

# Define the DNA alphabet
alphabet = ["A", "C", "G", "T"]
nucleotide_to_index = {nuc: idx for idx, nuc in enumerate(alphabet)}
index_to_nucleotide = {idx: nuc for nuc, idx in nucleotide_to_index.items()}

# Define HMM parameters
n_states = 3  # Match, Insertion, Deletion

# Transition probabilities
trans_probs = np.array([
    [0.7, 0.2, 0.1],  # Match -> Match, Insert, Delete
    [0.3, 0.4, 0.3],  # Insert -> Match, Insert, Delete
    [0.5, 0.1, 0.4],  # Delete -> Match, Insert, Delete
])

# Emission probabilities
emission_probs = np.array([
    [0.25, 0.25, 0.25, 0.25],  # Insert: Random emission
    [0.1, 0.4, 0.4, 0.1],      # Insert: Prefer C and G
    [0.0, 0.0, 0.0, 0.0],       # Delete: No emission
])

# Initial state probabilities
start_probs = np.array([0.8, 0.1, 0.1])  # Most likely to start in Match

# Create the HMM model
model = hmm.MultinomialHMM(n_components=n_states, n_iter=100, tol=0.01)
model.startprob_ = start_probs
model.transmat_ = trans_probs
model.emissionprob_ = emission_probs
model.n_trials = 1


# Function to generate a mutated sequence
def generate_mutated_sequence(original_sequence):
    # Capitalize the input sequence
    original_sequence = original_sequence.upper()

    # Encode sequence length
    seq_length = len(original_sequence)

    # Simulate the HMM state sequence
    state_sequence, _ = model.sample(seq_length)

    mutated_sequence = []
    for i, state in enumerate(state_sequence):
        if state[0] == 0:  # Match state
            mutated_sequence.append(original_sequence[i])  # Keep original nucleotide
        elif state[0] == 1:  # Insert state
            # Randomly select a nucleotide based on Insert emission probabilities
            random_nucleotide = random.choices(
                population=alphabet,
                weights=emission_probs[1],
                k=1
            )[0]
            mutated_sequence.append(random_nucleotide)
        elif state[0] == 2:  # Delete state
            # Skip this nucleotide (no output)
            continue

    return "".join(mutated_sequence)

# Read the original CSV file with sequences
df = pd.read_csv('dna_sequences.csv')  # Assuming sequences are in a column named 'sequence1'

# Generate mutated sequences using the HMM model
df['Generated'] = df['sequence1'].apply(generate_mutated_sequence)

# Save the results to a new CSV file
df.to_csv('mutated_sequences.csv', index=False)

print("Mutated sequences saved to 'mutated_sequences.csv'.")
