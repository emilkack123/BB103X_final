import argparse
import pandas as pd
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Generate a boxplot from hydrophobicity results.")
    parser.add_argument("--csv", type=str, required=True,
                        help="Path to the CSV file with hydrophobicity results.")
    parser.add_argument("--output", type=str, default="results/hydrophobicity_boxplot.png",
                        help="Filename to save the output boxplot image.")
    parser.add_argument("--show", action="store_true", help="Display the plot after saving.")
    args = parser.parse_args()

    # Load data
    df = pd.read_csv(args.csv)

    # Ensure required columns exist
    if 'Hydrophobicity' not in df.columns or 'Type' not in df.columns:
        raise ValueError("CSV must contain 'Hydrophobicity' and 'Type' columns.")

    # Drop missing values
    df = df.dropna(subset=['Hydrophobicity', 'Type'])

    # Create boxplot
    df.boxplot(column='Hydrophobicity', by='Type')
    plt.title('Hydrophobicity by Sequence Type')
    plt.suptitle('')
    plt.ylabel('Hydrophobicity')

    # Save and optionally show
    plt.savefig(args.output)
    print(f"Boxplot saved as {args.output}")
    if args.show:
        plt.show()

if __name__ == "__main__":
    main()
