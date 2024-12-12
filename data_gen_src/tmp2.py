import pandas as pd

# Read the CSV file
df = pd.read_csv('mutated_sequences.csv')  # Replace with your actual file name

# Convert all string columns to uppercase
df = df.applymap(lambda x: x.upper() if isinstance(x, str) else x)

# Save the updated DataFrame to a new CSV file
df.to_csv('mutated_sequences.csv', index=False)

print("All lowercase characters have been converted to uppercase.")
