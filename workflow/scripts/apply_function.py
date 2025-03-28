import pandas as pd
import argparse

def merge_data(hydro_file, pi_file, mol_weight_file, tm_score_file):
    """ Merge hydrophobicity, pI, molecular weight, and TM-score data based on ID and Sequence """

    # Load CSV files
    hydro_df = pd.read_csv(hydro_file)
    pi_df = pd.read_csv(pi_file)
    mol_weight_df = pd.read_csv(mol_weight_file)
    tm_score_df = pd.read_csv(tm_score_file)

    # Standardize column names
    hydro_df.columns = hydro_df.columns.str.upper()
    pi_df.columns = pi_df.columns.str.upper()
    mol_weight_df.columns = mol_weight_df.columns.str.upper()
    tm_score_df.columns = tm_score_df.columns.str.upper()

    # Rename "Sequence_ID" to "ID" in molecular weight data for consistency
    mol_weight_df.rename(columns={"SEQUENCE_ID": "ID"}, inplace=True)
    tm_score_df.rename(columns={"ID_SEQUENCES": "ID"}, inplace=True)

    # Merge datasets on ID and Sequence where applicable
    merged_df = pd.merge(hydro_df, pi_df, on=["ID", "SEQUENCE"], how="inner")
    merged_df = pd.merge(merged_df, mol_weight_df, on=["ID"], how="inner")
    merged_df = pd.merge(merged_df, tm_score_df, on=["ID"], how="inner")

     # **Fix TM-SCORE column: Remove extra text (anything after space or '(')**
    merged_df["TM-SCORE"] = merged_df["TM-SCORE"].astype(str).str.split(" ").str[0]
    merged_df["TM-SCORE"] = pd.to_numeric(merged_df["TM-SCORE"], errors="coerce")  # Convert to float

    return merged_df

def parse_args():
    parser = argparse.ArgumentParser(description="Merge hydrophobicity, pI, molecular weight, and TM-score data.")
    parser.add_argument("hydro_file", help="Path to the CSV file containing hydrophobicity values")
    parser.add_argument("pi_file", help="Path to the CSV file containing pI values")
    parser.add_argument("mol_weight_file", help="Path to the CSV file containing molecular weight values")
    parser.add_argument("tm_score_file", help="Path to the CSV file containing TM-score values")  # ADD TM-score FILE
    parser.add_argument("--output_file", default="merged_results.csv", help="Path to save the merged output CSV")
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Pass all four input files (Hydrophobicity, pI, Molecular Weight, TM-score)
    merged_df = merge_data(args.hydro_file, args.pi_file, args.mol_weight_file, args.tm_score_file)

    # Save merged results
    merged_df.to_csv(args.output_file, index=False)
    print(f"Merged results saved to {args.output_file}")

if __name__ == "__main__":
    main()