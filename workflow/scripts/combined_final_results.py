import pandas as pd
import argparse
import os

def extract_affinity(docking_file):
    try:
        with open(docking_file, 'r') as f:
            for line in f:
                if "Docking Score (Energy):" in line:
                    parts = line.split(":")[1].strip()
                    parts = parts.strip("[]").split()
                    if parts:
                        return float(parts[0])
        return None
    except Exception as e:
        print(f"Error reading {docking_file}: {e}")
        return None

def merge_data(hydro_file, pi_file, mol_weight_file, tm_score_file, stability_file, docking_dir):
    # Load data
    hydro_df = pd.read_csv(hydro_file)
    pi_df = pd.read_csv(pi_file)
    mol_weight_df = pd.read_csv(mol_weight_file)
    tm_score_df = pd.read_csv(tm_score_file)
    stability_df = pd.read_csv(stability_file)

    # Standardize column names
    for df in [hydro_df, pi_df, mol_weight_df, tm_score_df, stability_df]:
        df.columns = df.columns.str.upper()

    mol_weight_df.rename(columns={"SEQUENCE_ID": "ID"}, inplace=True)
    tm_score_df.rename(columns={"ID_SEQUENCES": "ID"}, inplace=True)

    for df in [hydro_df, pi_df, mol_weight_df, tm_score_df]:
        if "TYPE" in df.columns:
            df.drop(columns=["TYPE"], inplace=True)

    # Merge everything
    merged_df = pd.merge(hydro_df, pi_df, on=["ID", "SEQUENCE"], how="left")
    merged_df = pd.merge(merged_df, mol_weight_df, on=["ID"], how="left")
    merged_df = pd.merge(merged_df, tm_score_df, on=["ID"], how="left")
    merged_df = pd.merge(merged_df, stability_df, on=["ID"], how="left")

    # Clean TM_SCORE
    merged_df["TM_SCORE"] = merged_df["TM_SCORE"].astype(str).str.split(" ").str[0]
    merged_df["TM_SCORE"] = pd.to_numeric(merged_df["TM_SCORE"], errors="coerce")

    # Fill missing values
    for col in ["HYDROPHOBICITY", "PI", "MOLECULAR_WEIGHT", "TM_SCORE", "STABILITY"]:
        if col in merged_df.columns:
            merged_df[col].fillna(0, inplace=True)

    # Add AFFINITY
    def get_affinity(row):
        if row.get("TYPE", "").lower() == "generated":
            docking_file = os.path.join(docking_dir, f"docking_results_{row['ID']}.txt")
            return extract_affinity(docking_file)
        else:
            return 0.0  # Natural sequences get 0

    merged_df["AFFINITY"] = merged_df.apply(get_affinity, axis=1)

    return merged_df

def parse_args():
    parser = argparse.ArgumentParser(description="Merge data and extract affinity from docking results.")
    parser.add_argument("hydro_file")
    parser.add_argument("pi_file")
    parser.add_argument("mol_weight_file")
    parser.add_argument("tm_score_file")
    parser.add_argument("stability_file")
    parser.add_argument("docking_dir", help="Directory containing docking result .txt files")
    parser.add_argument("--output_file", default="merged_results.csv")
    return parser.parse_args()

def main():
    args = parse_args()
    df = merge_data(
        args.hydro_file, args.pi_file, args.mol_weight_file,
        args.tm_score_file, args.stability_file, args.docking_dir
    )
    df.to_csv(args.output_file, index=False)
    print(f"Merged file saved to {args.output_file}")

if __name__ == "__main__":
    main()

