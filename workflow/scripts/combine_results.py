import pandas as pd

# File paths
pi_file = "results/pI_results.csv"
hydro_file = "results/hydrophobicity_results.csv"
mw_file = "results/molecular_weight.csv"
fa_file = "resources/rubisco_sequences/nat.fa"
output_file = "results/filtered_results.csv"

# Function to extract sequence IDs from FASTA file
def read_fasta_ids(fasta_path):
    fasta_ids = set()
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):  
                fasta_id = line.split()[0].lstrip('>')  # Keep only the first part of the ID
                fasta_ids.add(fasta_id.strip())  # Remove spaces and store
    return fasta_ids

# Get sequence IDs to exclude
excluded_ids = read_fasta_ids(fa_file)

# Read CSV files
df_pi = pd.read_csv(pi_file)
df_hydro = pd.read_csv(hydro_file)
df_mw = pd.read_csv(mw_file)

# Merge pI and Hydrophobicity on 'ID'
df_merged = pd.merge(df_pi[['ID', 'pI']], df_hydro[['ID', 'Hydrophobicity']], on='ID')

# Normalize ID format (strip spaces, ensure consistent case)
df_merged['ID'] = df_merged['ID'].str.strip()

# Filter out sequences present in nat.fa
df_filtered = df_merged[~df_merged['ID'].isin(excluded_ids)]

# Read molecular weight data (filtering for Type == "Generated")
df_mw_filtered = df_mw[df_mw['Type'] == "Generated"][['Sequence_ID', 'Sequence_Length', 'Molecular_Weight']]

# Rename 'Sequence_ID' to 'ID' for merging consistency
df_mw_filtered = df_mw_filtered.rename(columns={'Sequence_ID': 'ID'})

# Merge molecular weight and sequence length data with the filtered dataset
df_final = pd.merge(df_filtered, df_mw_filtered, on='ID', how='left')

# Save the final filtered DataFrame
df_final.to_csv(output_file, index=False)

print(f"Final filtered CSV saved to {output_file}, {len(df_final)} sequences retained.")
