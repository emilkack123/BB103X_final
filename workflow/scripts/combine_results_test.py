import pandas as pd
import argparse

# Function to extract sequence IDs from FASTA file
def read_fasta_ids(fasta_path):
    fasta_ids = set()
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                fasta_id = line.split()[0].lstrip('>')  # Keep only the first part of the ID
                fasta_ids.add(fasta_id.strip())  # Remove spaces and store
    return fasta_ids

# Set up argument parsing
parser = argparse.ArgumentParser(description="Filter and merge biological data files.")
parser.add_argument('--pi_file', type=str, default="results/pI_results.csv", help="Path to the pI results CSV file")
parser.add_argument('--hydro_file', type=str, default="results/hydrophobicity_results.csv", help="Path to the Hydrophobicity results CSV file")
parser.add_argument('--mw_file', type=str, default="results/molecular_weight.csv", help="Path to the Molecular Weight results CSV file")
parser.add_argument('--tm_score_file', type=str, default="results/tm_scores/tm_score_gen_seq.csv", help="Path to the TM-score results CSV file")
parser.add_argument('--fa_file', type=str, default="resources/rubisco_sequences/nat.fa", help="Path to the FASTA file with sequence IDs to exclude")
parser.add_argument('--output_file', type=str, default="results/filtered_results.csv", help="Path to save the filtered results CSV file")

args = parser.parse_args()

# Get sequence IDs to exclude
excluded_ids = read_fasta_ids(args.fa_file)

# Read CSV files
df_pi = pd.read_csv(args.pi_file)
df_hydro = pd.read_csv(args.hydro_file)
df_mw = pd.read_csv(args.mw_file)
df_tm = pd.read_csv(args.tm_score_file)  # Load TM-score file

# Clean TM-score data (remove extra text from TM-score values)
df_tm['TM-score'] = df_tm['TM-score'].astype(str).str.split().str[0]  # Extract numerical value

# Merge pI and Hydrophobicity on 'ID'
df_merged = pd.merge(df_pi[['ID', 'pI']], df_hydro[['ID', 'Hydrophobicity']], on='ID')

# Normalize ID format (strip spaces, ensure consistent case)
df_merged['ID'] = df_merged['ID'].str.strip()
df_tm['Sequence ID'] = df_tm['Sequence ID'].str.strip()  # Ensure consistency in IDs

# Filter out sequences present in nat.fa
df_filtered = df_merged[~df_merged['ID'].isin(excluded_ids)]

# Read molecular weight data (filtering for Type == "Generated")
df_mw_filtered = df_mw[df_mw['Type'] == "Generated"][['Sequence_ID', 'Sequence_Length', 'Molecular_Weight']]

# Rename 'Sequence_ID' to 'ID' for merging consistency
df_mw_filtered = df_mw_filtered.rename(columns={'Sequence_ID': 'ID'})

# Merge molecular weight and sequence length data with the filtered dataset
df_final = pd.merge(df_filtered, df_mw_filtered, on='ID', how='left')

# Merge TM-score data based on matching sequence IDs
df_final = pd.merge(df_final, df_tm.rename(columns={'Sequence ID': 'ID'}), on='ID', how='left')

# Save the final filtered DataFrame
df_final.to_csv(args.output_file, index=False)

print(f"Final filtered CSV saved to {args.output_file}, {len(df_final)} sequences retained.")
