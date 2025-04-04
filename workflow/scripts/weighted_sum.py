import pandas as pd
import argparse

def apply_weighted_sum(input_file, output_file, a, b, c, d, e, f):
    """ Apply weighted sum formula with normalization based on natural sequence averages """
    
    # Load data
    df = pd.read_csv(input_file)

    # Normalize column names (convert to uppercase and remove whitespace)
    df.columns = df.columns.str.strip().str.upper()

    # Print column names for debugging
    print("Normalized Columns in dataset:", df.columns)

    # Convert relevant columns to numeric (forcing errors to NaN)
    cols_to_convert = [
        "HYDROPHOBICITY", "PI", "SEQUENCE_LENGTH", "MOLECULAR_WEIGHT", 
        "TM_SCORE", "STABILITY"
    ]
    
    for col in cols_to_convert:
        if col in df.columns:  # Ensure the column exists
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert and set errors as NaN

    # Handle NaN values (replace with 0 to avoid calculation errors)
    df.fillna(0, inplace=True)

    ### **Compute averages of natural sequences**
    natural_df = df[df["TYPE"].str.lower() == "natural"]  # Filter natural sequences
    avg_hydro = natural_df["HYDROPHOBICITY"].mean()
    avg_pi = natural_df["PI"].mean()
    avg_seq_length = natural_df["SEQUENCE_LENGTH"].mean()
    avg_mol_weight = natural_df["MOLECULAR_WEIGHT"].mean()

    ### **Compute weighted sum with absolute difference**
    df["WEIGHTED_SUM"] = (
        a * abs(df["HYDROPHOBICITY"] - avg_hydro) + 
        b * abs(df["PI"] - avg_pi) +
        c * abs(df["SEQUENCE_LENGTH"] - avg_seq_length) +
        d * abs(df["MOLECULAR_WEIGHT"] - avg_mol_weight) +
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
