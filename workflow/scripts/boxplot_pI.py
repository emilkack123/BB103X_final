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

    # Determine which column to use for pI values
    if 'pI' in df.columns:
        pI_values = df['pI']
    else:
        # If there is more than one column, use the second column; otherwise, use the first column.
        pI_values = df.iloc[:, 1] if df.shape[1] > 1 else df.iloc[:, 0]

    # Extract groups based on row positions:
    # Rows 2–11 (indices 1–10) correspond to "Generated"
    group_generated = pI_values.iloc[1:11]
    # Rows 12–21 (indices 11–20) correspond to "Natural"
    group_natural = pI_values.iloc[11:21]

    # Prepare data and labels for the boxplot
    data = [group_generated, group_natural]
    labels = ['Generated', 'Natural']

    # Create the boxplot
    plt.figure(figsize=(8, 6))
    plt.boxplot(data, labels=labels)
    plt.ylabel('pI-value')
    plt.title('Boxplot of pI-results')
    
    # Save the figure using the provided output filename
    plt.savefig(args.output)
    print(f"Boxplot saved as {args.output}")

if __name__ == "__main__":
    main()

