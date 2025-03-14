import pandas as pd

# Load RMSD results
input_file = "results/comparisons/rmsd_results_ahmad.txt"
output_file = "results/normalized_data_ahmad.txt"

# Read RMSD results
data = pd.read_csv(input_file, sep=":", names=["sequence", "rmsd"])

# Normalize RMSD values (0-1 scale)
data["normalized_rmsd"] = (data["rmsd"] - data["rmsd"].min()) / (data["rmsd"].max() - data["rmsd"].min())

# Save results
data.to_csv(output_file, sep="\t", index=False)

print(f"Normalized data saved to {output_file}")
