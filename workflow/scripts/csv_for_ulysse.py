import pandas as pd
from pathlib import Path
import re

# Basväg till data
base_path = Path("results")

# --- 1) Läs in alla fasta-ID från den sammanslagna fasta med både Natural & Generated ---
def extract_fasta_ids(filepath):
    with open(filepath, "r") as f:
        return [line[1:].strip().split()[0] for line in f if line.startswith(">")]

all_ids = extract_fasta_ids("results/gen+NaturalRubisco.fasta")
base_df = pd.DataFrame({"name": all_ids})

# --- 2) Läs in dina CSV-filer som tidigare ---
csv_files = {
    "confidence_scores": base_path / "confidence_scores.csv",
    "disorder_metrics": base_path / "disorder_metrics.csv",
    "hydrophobicity_results": base_path / "hydrophobicity_results.csv",
    "molecular_weight_results": base_path / "molecular_weight_results.csv",
    "pI_results": base_path / "pI_results.csv",
    "tm_scores": base_path / "tm-scores.csv",
    # Vi kommer göra PDB-mergen separat
    "metrics_only": base_path  
}

# Läs in metrics-CSVs
metrics = {
    "confidence_scores": pd.read_csv(csv_files["confidence_scores"]).rename(columns={"ID":"name"}),
    "disorder_metrics": pd.read_csv(csv_files["disorder_metrics"]).rename(columns={"id":"name"}),
    "hydrophobicity_results": pd.read_csv(csv_files["hydrophobicity_results"]).rename(columns={"ID":"name"}),
    "molecular_weight_results": pd.read_csv(csv_files["molecular_weight_results"]).rename(columns={"Sequence_ID":"name"}),
    "pI_results": pd.read_csv(csv_files["pI_results"]).rename(columns={"Sequence_ID":"name"}),
    "tm_scores": pd.read_csv(csv_files["tm_scores"]).rename(columns={"ID":"name"})
}

# --- 3) Slå ihop metrics på base_df ---
merged = base_df.copy()
for df in metrics.values():
    merged = merged.merge(df, how="left", on="name")

# --- 4) Slå på PDB-filen (endast de som finns) ---
pdb_df = pd.read_csv(base_path / "sequences_with_pdbs.csv").rename(columns={"seq_id":"name"})
merged = merged.merge(pdb_df, how="left", on="name")

# --- 5) Klassificera Type via ursprungliga fasta ---
gen_ids = extract_fasta_ids("resources/rubisco_sequences/dragon_radii_updated_704.fasta")
nat_ids = extract_fasta_ids("resources/rubisco_sequences/NaturalRubisco_shorten.fasta")

def to_base(x):
    # tar bort suffix .1/.2 etc
    x0 = x.split("_")[0]
    return re.sub(r"\.\d+$", "", x0)

gen_base = {to_base(x) for x in gen_ids}
nat_base = {to_base(x) for x in nat_ids}

def classify(name):
    b = to_base(name)
    if b in nat_base:
        return "Natural"
    elif b in gen_base:
        return "Generated"
    else:
        return "Unknown"

merged["Type"] = merged["name"].apply(classify)

# --- 6) pdb_path enligt Type ---
def make_path(row):
    if row["Type"]=="Generated":
        return f"~/dragon_radii_updated_all_pdb.tar.gz:{row['pdb_file']}"
    if row["Type"]=="Natural":
        return f"~/NaturalRubisco_shorten.tar.gz:{row['pdb_file']}"
    return ""

merged["pdb_path"] = merged.apply(make_path, axis=1)

# --- 7) Ordna kolumner & spara ---
cols = ["name","Type","pdb_file","pdb_path"] + [c for c in merged.columns if c not in ["name","Type","pdb_file","pdb_path"]]
merged[cols].to_csv(base_path / "combined_results_with_pdb_paths.csv", index=False)

# Diagnostik
print(merged["Type"].value_counts())
