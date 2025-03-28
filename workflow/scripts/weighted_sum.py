import pandas as pd
import argparse

def apply_weighted_sum(input_file, output_file, a, b, c, d, e):
    """ Apply weighted sum formula and save results """
    
    # Load data
    df = pd.read_csv(input_file)

    # Normalize column names (convert to uppercase and remove whitespace)
    df.columns = df.columns.str.strip().str.upper()

    # Print column names for debugging
    print("Normalized Columns in dataset:", df.columns)

    # Convert relevant columns to numeric (forcing errors to NaN)
    cols_to_convert = ["HYDROPHOBICITY", "PI", "SEQUENCE_LENGTH", "MOLECULAR_WEIGHT", "TM-SCORE"]
    for col in cols_to_convert:
        df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert and set errors as NaN

    # Handle NaN values (optional: replace with 0 or drop)
    df.fillna(0, inplace=True)  # Replace NaNs with 0 to avoid calculation errors

    # Compute weighted sum
    df["WEIGHTED_SUM"] = (
        a * df["HYDROPHOBICITY"] +
        b * df["PI"] +
        c * df["SEQUENCE_LENGTH"] +
        d * df["MOLECULAR_WEIGHT"] +
        e * df["TM-SCORE"]
    )

    # Save results
    df.to_csv(output_file, index=False)
    print(f"Weighted results saved to {output_file}")

def parse_args():
    parser = argparse.ArgumentParser(description="Compute weighted sum of properties")
    parser.add_argument("input_file", help="Path to input CSV file")
    parser.add_argument("output_file", help="Path to save the weighted results CSV")
    parser.add_argument("--a", type=float, default=1.0, help="Weight for Hydrophobicity")
    parser.add_argument("--b", type=float, default=1.0, help="Weight for pI")
    parser.add_argument("--c", type=float, default=1.0, help="Weight for Sequence Length")
    parser.add_argument("--d", type=float, default=1.0, help="Weight for Molecular Weight")
    parser.add_argument("--e", type=float, default=1.0, help="Weight for TM-SCORE")
    return parser.parse_args()

def main():
    args = parse_args()
    apply_weighted_sum(args.input_file, args.output_file, args.a, args.b, args.c, args.d, args.e)

if __name__ == "__main__":
    main()
