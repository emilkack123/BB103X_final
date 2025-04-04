import pandas as pd
import argparse
from sklearn.preprocessing import StandardScaler

def apply_weighted_sum(input_file, output_file, a, b, c, d, e, f):
    """ Apply weighted sum formula with Z-score normalization """

    # Load data
    df = pd.read_csv(input_file)

    # Normalize column names (convert to uppercase and remove whitespace)
    df.columns = df.columns.str.strip().str.upper()

    # Print column names for debugging
    print("Normalized Columns in dataset:", df.columns)

    # Define relevant columns
    cols_to_convert = [
        "HYDROPHOBICITY", "PI", "SEQUENCE_LENGTH", "MOLECULAR_WEIGHT", 
        "TM_SCORE", "STABILITY"
    ]

    # Filter existing columns
    existing_cols = [col for col in cols_to_convert if col in df.columns]

    if not existing_cols:
        raise ValueError("No relevant numeric columns found in the dataset.")

    # Convert relevant columns to numeric (forcing errors to NaN)
    df[existing_cols] = df[existing_cols].apply(pd.to_numeric, errors='coerce')

    # Handle NaN values (replace with column mean to avoid calculation errors)
    df[existing_cols] = df[existing_cols].apply(lambda x: x.fillna(x.mean()))

    # Compute averages of natural sequences (if 'TYPE' column exists)
    if "TYPE" in df.columns:
        natural_df = df[df["TYPE"].str.lower() == "natural"]
        if not natural_df.empty:
            avg_values = natural_df[existing_cols].mean()
        else:
            print("Warning: No 'natural' sequences found. Using global means.")
            avg_values = df[existing_cols].mean()
    else:
        print("Warning: 'TYPE' column missing. Using global means instead.")
        avg_values = df[existing_cols].mean()

    # Apply Z-score normalization
    scaler = StandardScaler()
    df[existing_cols] = scaler.fit_transform(df[existing_cols])

    # Compute weighted sum using normalized values
    df["WEIGHTED_SUM"] = (
        a * abs(df["HYDROPHOBICITY"] - avg_values["HYDROPHOBICITY"]) + 
        b * abs(df["PI"] - avg_values["PI"]) +
        c * abs(df["SEQUENCE_LENGTH"] - avg_values["SEQUENCE_LENGTH"]) +
        d * abs(df["MOLECULAR_WEIGHT"] - avg_values["MOLECULAR_WEIGHT"]) +
        e * df["TM_SCORE"] +
        f * df["STABILITY"]
    )

    # Save results
    df.to_csv(output_file, index=False)
    print(f"Weighted results saved to {output_file}")

def parse_args():
    parser = argparse.ArgumentParser(description="Compute weighted sum of properties with normalization")
    parser.add_argument("input_file", help="Path to input CSV file")
    parser.add_argument("output_file", help="Path to save the weighted results CSV")
    parser.add_argument("--a", type=float, default=1.0, help="Weight for Hydrophobicity")
    parser.add_argument("--b", type=float, default=1.0, help="Weight for pI")
    parser.add_argument("--c", type=float, default=1.0, help="Weight for Sequence Length")
    parser.add_argument("--d", type=float, default=1.0, help="Weight for Molecular Weight")
    parser.add_argument("--e", type=float, default=1.0, help="Weight for TM_SCORE")
    parser.add_argument("--f", type=float, default=1.0, help="Weight for Stability")
    return parser.parse_args()

def main():
    args = parse_args()
    apply_weighted_sum(args.input_file, args.output_file, args.a, args.b, args.c, args.d, args.e, args.f)

if __name__ == "__main__":
    main()
