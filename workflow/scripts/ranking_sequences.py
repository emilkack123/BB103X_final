import argparse
import pandas as pd

def rank_sequences(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)
    
    # Print the column names to verify they are as expected
    print("Columns in the input file:", df.columns)

    # Filter rows where the 'TYPE' column is 'generated'
    df_generated = df[df["TYPE"] == "GENERATED"]

    # Sort the sequences based on the WEIGHTED_SUM column in descending order
    df_sorted = df_generated.sort_values(by="WEIGHTED_SUM", ascending=False)

    # Add a ranking column
    df_sorted.insert(0, "RANKING", range(1, len(df_sorted) + 1))

    # Select only the relevant columns: RANKING, ID, and WEIGHTED_SUM
    df_sorted = df_sorted[["RANKING", "ID", "WEIGHTED_SUM"]]

    # Save the sorted sequences to a new CSV file
    df_sorted.to_csv(output_file, index=False)

    print(f"Ranked sequences that belong to 'generated' have been saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Rank sequences based on WEIGHTED_SUM and save to a new CSV file, filtering by 'generated' category.")
    parser.add_argument("input_file", help="Path to the input CSV file containing sequences and WEIGHTED_SUM values")
    parser.add_argument("output_file", help="Path to save the ranked sequences CSV file")

    args = parser.parse_args()
    
    rank_sequences(args.input_file, args.output_file)
