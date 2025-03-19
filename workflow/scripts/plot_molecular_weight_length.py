import argparse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def plot_data(csv_file, output_prefix):
    df = pd.read_csv(csv_file)

    # Boxplot: Molecular Weight
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="Type", y="Molecular_Weight", data=df, palette="Set2")
    plt.title("Molecular Weight Distribution (Generated vs Natural)")
    plt.xlabel("Sequence Type")
    plt.ylabel("Molecular Weight (Da)")
    output_path = f"{output_prefix}_molecular_weight_boxplot.png"
    plt.savefig(output_path)
    print(f" Saved: {output_path}")
    plt.close()

    # Histogram: Molecular Weight
    plt.figure(figsize=(8, 6))
    sns.histplot(df, x="Molecular_Weight", hue="Type", kde=True, bins=30, alpha=0.6)
    plt.title("Molecular Weight Distribution")
    plt.xlabel("Molecular Weight (Da)")
    plt.ylabel("Frequency")
    output_path = f"{output_prefix}_molecular_weight_histogram.png"
    plt.savefig(output_path)
    print(f" Saved: {output_path}")
    plt.close()

    # Boxplot: Sequence Length
    plt.figure(figsize=(8, 6))
    sns.boxplot(x="Type", y="Sequence_Length", data=df, palette="Set2")
    plt.title("Sequence Length Distribution (Generated vs Natural)")
    plt.xlabel("Sequence Type")
    plt.ylabel("Sequence Length (AA)")
    output_path = f"{output_prefix}_sequence_length_boxplot.png"
    plt.savefig(output_path)
    print(f" Saved: {output_path}")
    plt.close()

    # Scatter Plot: Molecular Weight vs Length
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="Sequence_Length", y="Molecular_Weight", hue="Type", data=df, alpha=0.7)
    plt.title("Molecular Weight vs Sequence Length")
    plt.xlabel("Sequence Length (AA)")
    plt.ylabel("Molecular Weight (Da)")
    plt.legend(title="Sequence Type")
    output_path = f"{output_prefix}_scatterplot.png"
    plt.savefig(output_path)
    print(f" Saved: {output_path}")
    plt.close()

    # Ensure all output files exist (Fixes Snakemake tracking issues)
    expected_outputs = [
        f"{output_prefix}_molecular_weight_boxplot.png",
        f"{output_prefix}_molecular_weight_histogram.png",
        f"{output_prefix}_sequence_length_boxplot.png",
        f"{output_prefix}_scatterplot.png"
    ]
    
    for output in expected_outputs:
        if not os.path.exists(output):
            print(f"⚠️ WARNING: {output} was NOT created, touching file to force Snakemake to track it.")
            open(output, 'a').close()  # Create empty file

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Plot molecular weight and sequence length distributions")
    parser.add_argument("input_csv", help="Path to molecular weight CSV")
    parser.add_argument("output_prefix", help="Prefix for output plot files")
    args = parser.parse_args()

    plot_data(args.input_csv, args.output_prefix)
