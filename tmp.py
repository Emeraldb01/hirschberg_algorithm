import random
import csv

def generate_random_dna(length):
    """Generate a random DNA sequence of a given length."""
    return ''.join(random.choices('ACGT', k=length))

def introduce_mutations(sequence, mutation_rate=0.01):
    """Introduce random mutations into a DNA sequence."""
    sequence = list(sequence)
    for i in range(len(sequence)):
        if random.random() < mutation_rate:
            mutation_type = random.choice(['substitution', 'insertion', 'deletion'])
            if mutation_type == 'substitution':
                sequence[i] = random.choice('ACGT'.replace(sequence[i], ''))
            elif mutation_type == 'insertion':
                sequence.insert(i, random.choice('ACGT'))
            elif mutation_type == 'deletion':
                sequence[i] = ''
    return ''.join(sequence)

def generate_dna_pairs(num_pairs, sequence_length, mutation_rate):
    """Generate pairs of DNA sequences with one sequence mutated."""
    pairs = []
    for _ in range(num_pairs):
        original = generate_random_dna(sequence_length)
        mutated = introduce_mutations(original, mutation_rate)
        pairs.append((original, mutated))
    return pairs

def save_to_csv(pairs, filename):
    """Save DNA sequence pairs to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['sequence1', 'sequence2'])
        # Write the DNA sequence pairs
        writer.writerows(pairs)

# Parameters
num_pairs = 200       # Number of pairs
sequence_length = 3000  # Length of each DNA sequence
mutation_rate = 0.01    # Mutation rate (1%)

# Generate and save data
dna_pairs = generate_dna_pairs(num_pairs, sequence_length, mutation_rate)
save_to_csv(dna_pairs, "synthetic_dna_pairs.csv")

print("DNA sequence pairs saved to 'synthetic_dna_pairs.csv'.")

