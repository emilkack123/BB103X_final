import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def plot_histogram(input_file, output_file):
    # Load the CSV file
    df = pd.read_csv(input_file)

    # Calculate sequence lengths
    df["length"] = df["sequence"].apply(len)

    # Separate the data into two categories
    generated_lengths = df[df["origin"] == "generated"]["length"]
    natural_lengths = df[df["origin"] == "natural"]["length"]

    # Plot the histograms
    plt.figure(figsize=(10, 6))
    sns.histplot(generated_lengths, bins=20, color="blue", alpha=0.6, label="Generated")
    sns.histplot(natural_lengths, bins=20, color="green", alpha=0.6, label="Natural")

    plt.xlabel("Sequence Length")
    plt.ylabel("Frequency")
    plt.title("Histogram of Sequence Lengths")
    plt.legend()

    # Save the plot as an image
    plt.savefig(output_file, dpi=300)
    plt.close()

    print(f"Histogram saved as {output_file}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate a histogram of sequence lengths.")
    parser.add_argument("input_file", type=str, help="Path to the input CSV file")
    parser.add_argument("output_file", type=str, help="Path to save the output histogram image")

    # Parse arguments
    args = parser.parse_args()

    # Run the function with the provided arguments
    plot_histogram(args.input_file, args.output_file)
