import os
from vina import Vina

# Coordinates and box size for the docking
cx = 0  # Center x-coordinate
cy = 0  # Center y-coordinate
cz = 0  # Center z-coordinate
bx = 20  # Box size in x direction 
by = 20  # Box size in y direction 
bz = 20  # Box size in z direction 

# Folder containing PDBQT files for receptors
receptor_folder = 'results/converted_pdbqt'

# Constant ligand file
ligand_file = 'results/docking/co2.pdbqt'

# Output folder for docking results
output_folder = 'results/docking'

# Initialize Vina object
v = Vina(sf_name='vina')

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Loop over all PDBQT files in the receptor folder
for receptor_file in os.listdir(receptor_folder):
    # Check if the file is a PDBQT file
    if receptor_file.endswith('.pdbqt'):
        receptor_path = os.path.join(receptor_folder, receptor_file)
        
        # Set the receptor and ligand
        v.set_receptor(receptor_path)
        v.set_ligand_from_file(ligand_file)

        # Compute maps for docking
        v.compute_vina_maps(center=[cx, cy, cz], box_size=[bx, by, bz])

        # Perform docking
        v.dock(exhaustiveness=20, n_poses=20)

        # Define the output filenames for the docked poses and minimized pose
        docked_filename = os.path.join(output_folder, f'docked_{receptor_file}')
        minimized_filename = os.path.join(output_folder, f'minimized_{receptor_file}')

        # Write docked poses to file
        v.write_poses(docked_filename, n_poses=5, energy_range=6.0, overwrite=True)

        # Get the docking score (energy)
        energy = v.score()

        # Perform optimization of the ligand in the receptor's binding site
        energy_minimized = v.optimize()

        # Write the minimized pose to file
        v.write_pose(minimized_filename, overwrite=True)

        # Save the results to a text file
        with open(os.path.join(output_folder, f'docking_results_{receptor_file}.txt'), 'w') as f:
            # Write the docking score (energy)
            f.write(f'Receptor: {receptor_file}\n')
            f.write(f'Docking Score (Energy): {energy}\n')
            
            # Write the minimized energy
            f.write(f'Minimized Energy: {energy_minimized}\n')
            
            # Optionally, write some more details about the docking process
            f.write('\nDocking completed successfully.\n')
            f.write(f'Top 5 poses have been written to {docked_filename}.\n')
            f.write(f'Minimized pose has been written to {minimized_filename}.\n')

        print(f"Docking results for {receptor_file} saved to {docked_filename} and {minimized_filename}.")

print("Docking for all receptors completed successfully.")
