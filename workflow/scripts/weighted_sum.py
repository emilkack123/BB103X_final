import pandas as pd
import argparse

def apply_weighted_sum(input_file, output_file, a, b, c, d):
    """ Compute weighted sum of Hydrophobicity, pI, Sequence_Length, and Molecular_Weight """

    # Load the merged CSV file
    df = pd.read_csv(input_file)

    # Ensure required columns exist
    required_columns = {"ID", "HYDROPHOBICITY", "PI", "SEQUENCE_LENGTH", "MOLECULAR_WEIGHT"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing required columns in input file. Expected: {required_columns}")

    # Compute the weighted sum
    df["Weighted_Score"] = (
        a * df["HYDROPHOBICITY"] + 
        b * df["PI"] + 
        c * df["SEQUENCE_LENGTH"] + 
        d * df["MOLECULAR_WEIGHT"]
    )

    # Save to a new CSV file with only ID and Weighted_Score
    df[["ID", "Weighted_Score"]].to_csv(output_file, index=False)
    print(f"Weighted scores saved to {output_file}")

def parse_args():
    parser = argparse.ArgumentParser(description="Compute weighted sum of biological properties.")
    parser.add_argument("input_file", help="Path to the merged CSV file containing the properties")
    parser.add_argument("output_file", help="Path to save the results CSV")
    parser.add_argument("--a", type=float, default=1.0, help="Weight for Hydrophobicity (default: 1.0)")
    parser.add_argument("--b", type=float, default=1.0, help="Weight for pI (default: 1.0)")
    parser.add_argument("--c", type=float, default=1.0, help="Weight for Sequence Length (default: 1.0)")
    parser.add_argument("--d", type=float, default=1.0, help="Weight for Molecular Weight (default: 1.0)")
    return parser.parse_args()

def main():
    args = parse_args()
    apply_weighted_sum(args.input_file, args.output_file, args.a, args.b, args.c, args.d)

if __name__ == "__main__":
    main()