import MDAnalysis as mda
from MDAnalysis.analysis.rms import RMSD
import numpy as np

# Lists of PDB filenames
generated_pdbs = ["gen1.pdb", "gen2.pdb", "gen3.pdb"]  # Add all AI-generated structures
natural_pdbs = ["nat1.pdb", "nat2.pdb", "nat3.pdb"]    # Add all natural structures

rmsd_matrix = np.zeros((len(generated_pdbs), len(natural_pdbs)))

# Loop over all AI-generated and natural structures
for i, gen_pdb in enumerate(generated_pdbs):
    gen = mda.Universe(gen_pdb)
    
    for j, nat_pdb in enumerate(natural_pdbs):
        nat = mda.Universe(nat_pdb)

        # Compute RMSD (aligning backbone atoms)
        rmsd_calc = RMSD(gen, nat, select="backbone")
        rmsd_calc.run()
        
        # Store RMSD value
        rmsd_value = rmsd_calc.rmsd[-1, 2]  # Last frame RMSD
        rmsd_matrix[i, j] = rmsd_value

# Save RMSD matrix to a CSV file
np.savetxt("rmsd_matrix.csv", rmsd_matrix, delimiter=",", header=",".join(natural_pdbs), comments='')

# Save best matches to a text file
best_matches = np.argmin(rmsd_matrix, axis=1)
with open("best_matches.txt", "w") as f:
    for i, best_j in enumerate(best_matches):
        f.write(f"{generated_pdbs[i]} best matches with {natural_pdbs[best_j]} (RMSD = {rmsd_matrix[i, best_j]:.3f} Å)\n")

print("RMSD matrix saved as 'rmsd_matrix.csv'. Best matches saved as 'best_matches.txt'.")
