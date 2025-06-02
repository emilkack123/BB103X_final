import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Set up argparse to handle command-line parameters
    parser = argparse.ArgumentParser(description="Generate a boxplot from pI values in a CSV file.")
    parser.add_argument("--csv", type=str, default="results/pI_results.csv",
                        help="Path to the CSV file containing pI results (default: results/pI_results.csv)")
    parser.add_argument("--output", type=str, default="boxplot.png",
                        help="Filename for saving the output boxplot image (default: boxplot.png)")
    args = parser.parse_args()

    # Read the CSV file
    df = pd.read_csv(args.csv)

    # Check that necessary columns exist
    if 'pI' not in df.columns or 'Type' not in df.columns:
        raise ValueError("CSV must contain 'pI' and 'Type' columns.")

    # Separate data based on Type column
    group_generated = df[df['Type'] == 'Generated']['pI']
    group_natural = df[df['Type'] == 'Natural']['pI']

    # Prepare data and labels
    data = [group_generated.dropna(), group_natural.dropna()]
    labels = ['Generated', 'Natural']

    # Create boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels)
    plt.ylabel('pI-value')
    plt.title('Boxplot of pI-results')
    plt.tight_layout()
    plt.savefig(args.output)
    print(f"Boxplot saved as {args.output}")

if __name__ == "__main__":
    main()
