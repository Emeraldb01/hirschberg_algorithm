from hmmlearn import hmm
import numpy as np
import pandas as pd
import random

# Define the DNA alphabet
alphabet = ["A", "C", "G", "T"]
nucleotide_to_index = {nuc: idx for idx, nuc in enumerate(alphabet)}
index_to_nucleotide = {idx: nuc for nuc, idx in nucleotide_to_index.items()}

# Define HMM parameters
n_states = 4  # Match, Insertion, Deletion, Mismatch

# Base emission probabilities
emission_probs = np.array([
    [1.0, 0.0, 0.0, 0.0],  # Match: Original nucleotide (emission handled directly)
    [0.1, 0.4, 0.4, 0.1],  # Insert: Random nucleotide
    [1.0, 0.0, 0.0, 0.0],  # Delete: No emission
    [0.1, 0.4, 0.4, 0.1],  # Mismatch: Random nucleotide
])

# Function to configure HMM for different scenarios
def configure_hmm(trans_probs):
    model = hmm.MultinomialHMM(n_components=n_states, n_iter=100, tol=0.01)
    model.n_trials = 1  # Specify the number of trials per observation
    model.startprob_ = np.array([1.0, 0.0, 0.0, 0.0])  # Always start in Match
    model.transmat_ = trans_probs
    model.emissionprob_ = emission_probs
    return model

# Function to generate a mutated sequence
def generate_mutated_sequence(model, original_sequence):
    original_sequence = original_sequence.upper()
    seq_length = len(original_sequence)

    state_sequence, _ = model.sample(seq_length)
    # Extract state indices from the one-hot encoded state sequence
    state_sequence_indices = [np.argmax(state) for state in state_sequence]
    
    mutated_sequence = []

    for i, state in enumerate(state_sequence_indices):
        if state == 0:  # Match state
            mutated_sequence.append(original_sequence[i])
        elif state == 1:  # Insert state
            # Randomly decide how many nucleotides to insert (between 1 and 5)
            num_insertions = random.randint(1, 8)
            
            for _ in range(num_insertions):
                random_nucleotide = random.choices(population=alphabet, weights=emission_probs[1], k=1)[0]
                mutated_sequence.append(random_nucleotide)
        elif state == 2:  # Delete state
            continue  # Skip this nucleotide
        elif state == 3:  # Mismatch state
            random_nucleotide = random.choices(population=alphabet, weights=emission_probs[3], k=1)[0]
            mutated_sequence.append(random_nucleotide)

    return "".join(mutated_sequence)



# Custom configurations for each group
configs = [
    {"trans_probs": (
        [0.95, 0.005, 0.005, 0.04],  # Mostly Match
        [0.8, 0.2, 0.0, 0.0],
        [0.8, 0.0, 0.2, 0.0],
        [1.0, 0.0, 0.0, 0.0],
    )},
    {"trans_probs": (
        [0.6, 0.2, 0.1, 0.1],  # High Insert/Delete
        [0.8, 0.2, 0.0, 0.0],
        [0.5, 0.0, 0.5, 0.0],
        [0.7, 0.3, 0.0, 0.0],
    )},
    {"trans_probs": (
        [0.8, 0.2, 0.0, 0.0],  # Only Insert
        [0.7, 0.3, 0.0, 0.0],
        [0.7, 0.0, 0.3, 0.0],
        [0.7, 0.3, 0.0, 0.0],
    )},
    {"trans_probs": (
        [0.8, 0.0, 0.2, 0.0],  # Only Delete
        [0.7, 0.0, 0.3, 0.0],
        [0.5, 0.0, 0.5, 0.0],
        [0.7, 0.0, 0.3, 0.0],
    )},
    {"trans_probs": (
        [0.9, 0.0, 0.0, 0.1],  # Only Mismatch
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.8, 0.0, 0.0, 0.2],
    )},
]

# Read the original CSV file
df = pd.read_csv('data_gen_src/dna_sequences.csv')

# Generate sequences for each configuration
all_sequences = []
for idx, config in enumerate(configs):
    model = configure_hmm(config["trans_probs"])
    for _ in range(3):  # Generate 3 sequences per group
        df[f'Group_{idx+1}'] = df['sequence1'].apply(lambda seq: generate_mutated_sequence(model, seq))

# Save the results to a new CSV file
df.to_csv('mutated_sequences.csv', index=False)

print("Mutated sequences saved to 'mutated_sequences.csv'.")
