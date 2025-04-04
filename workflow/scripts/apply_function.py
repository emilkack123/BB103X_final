import pandas as pd
import argparse

def merge_data(hydro_file, pi_file, mol_weight_file, tm_score_file, stability_file):
    """ Merge multiple data files based on ID and Sequence, replacing missing values with 0 """

    # Load CSV files
    hydro_df = pd.read_csv(hydro_file)
    pi_df = pd.read_csv(pi_file)
    mol_weight_df = pd.read_csv(mol_weight_file)
    tm_score_df = pd.read_csv(tm_score_file)
    stability_df = pd.read_csv(stability_file)

    # Standardize column names
    for df in [hydro_df, pi_df, mol_weight_df, tm_score_df, stability_df]:
        df.columns = df.columns.str.upper()

    # Rename "SEQUENCE_ID" to "ID" in molecular weight data for consistency
    mol_weight_df.rename(columns={"SEQUENCE_ID": "ID"}, inplace=True)
    tm_score_df.rename(columns={"ID_SEQUENCES": "ID"}, inplace=True)

    # Drop TYPE from any other dataframe just to be safe
    for df in [hydro_df, pi_df, mol_weight_df, tm_score_df]:
        if "TYPE" in df.columns:
            df.drop(columns=["TYPE"], inplace=True)

    # Merge datasets using LEFT JOIN (to keep all IDs from hydrophobicity data)
    merged_df = pd.merge(hydro_df, pi_df, on=["ID", "SEQUENCE"], how="left")
    merged_df = pd.merge(merged_df, mol_weight_df, on=["ID"], how="left")
    merged_df = pd.merge(merged_df, tm_score_df, on=["ID"], how="left")
    merged_df = pd.merge(merged_df, stability_df, on=["ID"], how="left")  # TYPE comes from here

    # Fix TM_SCORE column: remove text after space or parentheses
    merged_df["TM_SCORE"] = merged_df["TM_SCORE"].astype(str).str.split(" ").str[0]
    merged_df["TM_SCORE"] = pd.to_numeric(merged_df["TM_SCORE"], errors="coerce")

    # Fill missing values in numerical columns with 0
    num_cols = ["HYDROPHOBICITY", "PI", "MOLECULAR_WEIGHT", "TM_SCORE", "STABILITY"]
    for col in num_cols:
        if col in merged_df.columns:
            merged_df[col].fillna(0, inplace=True)

    return merged_df

def parse_args():
    parser = argparse.ArgumentParser(description="Merge multiple data sources into one CSV.")
    parser.add_argument("hydro_file", help="Path to the CSV file containing hydrophobicity values")
    parser.add_argument("pi_file", help="Path to the CSV file containing pI values")
    parser.add_argument("mol_weight_file", help="Path to the CSV file containing molecular weight values")
    parser.add_argument("tm_score_file", help="Path to the CSV file containing TM_score values")
    parser.add_argument("stability_file", help="Path to the CSV file containing stability values")
    parser.add_argument("--output_file", default="merged_results.csv", help="Path to save the merged output CSV")
    return parser.parse_args()

def main():
    args = parse_args()
    
    merged_df = merge_data(
        args.hydro_file, args.pi_file, args.mol_weight_file, args.tm_score_file,
        args.stability_file
    )

    # Save merged results
    merged_df.to_csv(args.output_file, index=False)
    print(f"Merged results saved to {args.output_file}")

if __name__ == "__main__":
    main()