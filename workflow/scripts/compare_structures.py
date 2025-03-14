import os
import numpy as np

# Input and output directories
input_dir = "results/structures/"
output_file = "results/comparisons/rmsd_results_ahmad.txt"

# Ensure output directory exists
os.makedirs("results/comparisons", exist_ok=True)

# Placeholder RMSD calculation
rmsd_results = {}

for pdb_file in os.listdir(input_dir):
    if pdb_file.endswith(".pdb"):
        sequence_id = pdb_file.replace(".pdb", "")
        rmsd_value = np.random.uniform(0, 5)  # Simulating RMSD calculation
        rmsd_results[sequence_id] = rmsd_value

# Save RMSD results
with open(output_file, "w") as f_out:
    for seq, rmsd in rmsd_results.items():
        f_out.write(f"{seq}: {rmsd}\n")

print(f"RMSD results saved to {output_file}")
