import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main():
    # Set up argparse to handle command-line parameters.
    parser = argparse.ArgumentParser(description="Generate a boxplot from Hydrophobicity results in a CSV file.")
    parser.add_argument("--csv", type=str, default="results/Hydrophobicity_results.csv",
                        help="Path to the CSV file containing Hydrophobicity results (default: results/Hydrophobicity_results.csv)")
    parser.add_argument("--output", type=str, default="Hydrophobicity_boxplot.png",
                        help="Filename for saving the output boxplot image (default: Hydrophobicity_boxplot.png)")
    parser.add_argument("--show", action="store_true",
                        help="Display the plot after saving (default: False)")
    args = parser.parse_args()

    # Read the CSV file.
    df = pd.read_csv(args.csv)

    # If the file has a column 'Hydrophobicity', use it; otherwise, assume the values are in the second column.
    if 'Hydrophobicity' in df.columns:
        hydro_values = df['Hydrophobicity']
    else:
        hydro_values = df.iloc[:, 1] if df.shape[1] > 1 else df.iloc[:, 0]

    # Convert Hydrophobicity values to numeric, coercing errors to NaN, and drop NaN values.
    hydro_values = pd.to_numeric(hydro_values, errors='coerce').dropna()

    # Note: If the CSV has a header, then rows 2–11 correspond to data with indices 1–10,
    # and rows 12–21 correspond to data with indices 11–20.
    # Use the selected hydro_values for grouping.
    group_generated = hydro_values.iloc[0:10]
    group_natural = hydro_values.iloc[10:20]

    # Prepare the data and labels for the boxplot.
    data = [group_generated, group_natural]
    labels = ['Generated', 'Natural']

    # Create the boxplot.
    plt.boxplot(data, labels=labels)
    plt.ylabel('Hydrophobicity')
    plt.title('Boxplot of Hydrophobicity Results')
    plt.savefig(args.output)
    print(f"Boxplot saved as {args.output}")

    if args.show:
        plt.show()

if __name__ == "__main__":
    main()
