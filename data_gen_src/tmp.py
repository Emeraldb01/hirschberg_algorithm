import pandas as pd

# Function to reformat the CSV
def reformat_csv(input_csv, output_csv):
    # Load the original CSV
    df = pd.read_csv(input_csv)

    # Prepare a list to store rows for the new DataFrame
    rows = []

    # Iterate over each row in the original CSV
    for idx, row in df.iterrows():
        sequence1 = row['sequence1']

        # Append a new row for each group column
        for group_col in ['Group_1','Group_2', 'Group_3', 'Group_4', 'Group_5']:
            sequence2 = row[group_col]
            rows.append({'sequence1': sequence1, 'sequence2': sequence2})

    # Create a new DataFrame
    reformatted_df = pd.DataFrame(rows)

    # Save the reformatted DataFrame to a new CSV
    reformatted_df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    # Specify the input and output CSV file paths
    input_csv = "mutated_sequences.csv"
    output_csv = "reformatted_sequences.csv"

    # Reformat the CSV
    reformat_csv(input_csv, output_csv)

    print(f"Reformatted CSV saved to '{output_csv}'.")