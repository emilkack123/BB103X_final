import pandas as pd
import os

# File paths
pi_file = "results/pI_results.csv"
hydro_file = "results/hydrophobicity_results.csv"
mw_file = "results/molecular_weight.csv"
tm_score_file = "results/tm_scores/tm-scores.csv"  # TM-score file
conf_score_file = "results/confidence_scores.csv"  # Confidence scores file
fa_file = "resources/rubisco_sequences/nat.fa"
docking_results_folder = "results/docking"
output_file = "results/combined_results.csv"

# Function to extract sequence IDs from FASTA file
def read_fasta_ids(fasta_path):
    fasta_ids = set()
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                fasta_id = line.split()[0].lstrip('>')  # Keep only the first part of the ID
                fasta_ids.add(fasta_id.strip())  # Remove spaces and store
    return fasta_ids

# Function to extract docking affinity from the text file
def extract_affinity(docking_file):
    try:
        with open(docking_file, 'r') as f:
            for line in f:
                if "Docking Score (Energy):" in line:
                    # Extracting the first value of the energy list (affinity)
                    parts = line.split(":")[1].strip()  # Get the list part
                    parts = parts.strip("[]").split()  # Remove square brackets and split by spaces
                    if parts:  # Check if there are values in the list
                        affinity = float(parts[0])  # The first value is the affinity
                        return affinity
        return None  # If no affinity is found
    except Exception as e:
        print(f"Error reading {docking_file}: {e}")
        return None

# Get sequence IDs to exclude
excluded_ids = read_fasta_ids(fa_file)

# Read CSV files
df_pi = pd.read_csv(pi_file)
df_hydro = pd.read_csv(hydro_file)
df_mw = pd.read_csv(mw_file)
df_tm = pd.read_csv(tm_score_file)  # Load TM-score file
df_conf = pd.read_csv(conf_score_file)  # Load confidence scores file

# Clean TM-score data (remove extra text from TM-score values)
df_tm.rename(columns={'TM_SCORE': 'TM-score'}, inplace=True)

# Merge pI and Hydrophobicity on 'ID'
df_merged = pd.merge(df_pi[['ID', 'pI']], df_hydro[['ID', 'Hydrophobicity']], on='ID')

# Normalize ID format (strip spaces, ensure consistent case)
df_merged['ID'] = df_merged['ID'].str.strip()
df_tm['ID'] = df_tm['ID'].str.strip()
df_conf['ID'] = df_conf['ID'].str.strip()

# Filter out sequences present in nat.fa
df_filtered = df_merged[~df_merged['ID'].isin(excluded_ids)]

# Read molecular weight data (filtering for Type == "Generated")
df_mw_filtered = df_mw[df_mw['Type'] == "Generated"][['Sequence_ID', 'Sequence_Length', 'Molecular_Weight']]
df_mw_filtered = df_mw_filtered.rename(columns={'Sequence_ID': 'ID'})  # Rename for merging consistency

# Merge molecular weight and sequence length data with the filtered dataset
df_final = pd.merge(df_filtered, df_mw_filtered, on='ID', how='left')

# Merge TM-score data based on matching sequence IDs
df_final = pd.merge(df_final, df_tm, on='ID', how='left')

# Filter confidence scores to include only "GENERATED" sequences
df_conf_filtered = df_conf[df_conf['TYPE'] == "GENERATED"][['ID', 'STABILITY']]

# Merge confidence scores
df_final = pd.merge(df_final, df_conf_filtered, on='ID', how='left')

# Add the affinity (docking score) to the dataframe
affinity_list = []
for seq_id in df_final['ID']:
    docking_file = os.path.join(docking_results_folder, f"docking_results_{seq_id}.txt")
    print(f"Processing docking file for {seq_id}: {docking_file}")  # Debug line
    affinity = extract_affinity(docking_file)
    
    if affinity is not None:
        print(f"Affinity found for {seq_id}: {affinity}")  # Debug line
    else:
        print(f"Affinity NOT found for {seq_id}")  # Debug line
    
    affinity_list.append(affinity)

df_final['Affinity'] = affinity_list

# Save the final filtered DataFrame
df_final.to_csv(output_file, index=False)

print(f"Final filtered CSV saved to {output_file}, {len(df_final)} sequences retained.")
