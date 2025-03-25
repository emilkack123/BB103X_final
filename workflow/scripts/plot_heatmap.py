import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import argparse
import numpy as np

def plot_heatmap(input_file, output_file):
    # Read the file
    with open(input_file, "r") as f:
        lines = f.readlines()

    # Extract sequence IDs from the first column
    sequence_ids = [line.split()[0] for line in lines]

    # Add the missing header row
    header = "\t" + "\t".join(sequence_ids) + "\n"
    cleaned_lines = [header] + lines

    # Save cleaned data temporarily
    temp_file = input_file + "_cleaned.tsv"
    with open(temp_file, "w") as f:
        f.writelines(cleaned_lines)

    # Load the cleaned distance matrix
    df = pd.read_csv(temp_file, sep="\t", index_col=0)

    # Ensure all values are numeric
    df = df.apply(pd.to_numeric, errors="coerce").fillna(0)

    # Debugging: Print matrix details
    print("🔍 Distance matrix shape:", df.shape)
    print("🔍 Distance matrix first few rows:\n", df.head())

    # Ensure the matrix is square (NxN)
    if df.empty or df.shape[0] != df.shape[1]:
        raise ValueError(f"Error: Distance matrix is empty or not square! Shape: {df.shape}")

    # Plot heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(df, cmap="coolwarm", annot=False, linewidths=0.5)

    # Title
    plt.title("Rubisco Distance Matrix Heatmap")

    # Save plot
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"✅ Heatmap saved: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a heatmap from a distance matrix.")
    parser.add_argument("input_file", help="Path to the distance matrix (TSV file)")
    parser.add_argument("output_file", help="Path to save the heatmap")
    args = parser.parse_args()

    plot_heatmap(args.input_file, args.output_file)
