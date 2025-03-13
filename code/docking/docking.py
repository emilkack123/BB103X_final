from vina import Vina

# Coordinates and box size for the docking
cx = 0  # Center x-coordinate
cy = 0  # Center y-coordinate
cz = 0  # Center z-coordinate
bx = 20  # Box size in x direction 
by = 20  # Box size in y direction 
bz = 20  # Box size in z direction 

# Initialize Vina object
v = Vina(sf_name='vina')

# Set receptor and ligand files
v.set_receptor('/home/moa/BB103X_final/results/gen_structures/model_1.pdbqt')
v.set_ligand_from_file('/home/moa/BB103X_final/results/docking/co2.pdbqt')

# Compute maps for docking
v.compute_vina_maps(center=[cx, cy, cz], box_size=[bx, by, bz])

# Perform docking
v.dock(exhaustiveness=20, n_poses=20)

# Write docked poses to file
v.write_poses('/home/moa/BB103X_final/results/docking/docked_enzyme.pdbqt', n_poses=5, energy_range=6.0, overwrite=True)

# Get the docking score (energy)
energy = v.score()

# Perform optimization of the ligand in the receptor's binding site
energy_minimized = v.optimize()

# Write the minimized pose to file
v.write_pose('/home/moa/BB103X_final/results/docking/minimized.pdbqt', overwrite=True)

# Save the results to a text file
with open('/home/moa/BB103X_final/results/docking/docking_results.txt', 'w') as f:
    # Write the docking score (energy)
    f.write(f'Docking Score (Energy): {energy}\n')
    
    # Write the minimized energy
    f.write(f'Minimized Energy: {energy_minimized}\n')
    
    # Optionally, write some more details about the docking process
    f.write('\nDocking completed successfully.\n')
    f.write('Top 5 poses have been written to docked_enzyme.pdbqt.\n')
    f.write('Minimized pose has been written to minimized.pdbqt.\n')

print("Docking results saved to docking_results.txt.")
