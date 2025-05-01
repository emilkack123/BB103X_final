import argparse
from vina import Vina

# Parse arguments
parser = argparse.ArgumentParser(description='Dock a ligand to a receptor using AutoDock Vina')
parser.add_argument('--receptor_file', required=True)
parser.add_argument('--ligand_file', required=True)
parser.add_argument('--docked_output', required=True)
parser.add_argument('--minimized_output', required=True)
parser.add_argument('--result_output', required=True)
args = parser.parse_args()

# Box parameters (customize if needed)
cx, cy, cz = 0, 0, 0
bx, by, bz = 20, 20, 20

# Initialize Vina
v = Vina(sf_name='vina')

# Set receptor and ligand
v.set_receptor(args.receptor_file)
v.set_ligand_from_file(args.ligand_file)

# Compute docking maps
v.compute_vina_maps(center=[cx, cy, cz], box_size=[bx, by, bz])

# Run docking
v.dock(exhaustiveness=20, n_poses=20)
v.write_poses(args.docked_output, n_poses=5, energy_range=6.0, overwrite=True)

# Get energy and optimize
energy = v.score()
energy_minimized = v.optimize()
v.write_pose(args.minimized_output, overwrite=True)

# Save docking results
with open(args.result_output, 'w') as f:
    f.write(f'Receptor: {args.receptor_file}\n')
    f.write(f'Docking Score (Energy): {energy}\n')
    f.write(f'Minimized Energy: {energy_minimized}\n')
    f.write('\nDocking completed successfully.\n')
    f.write(f'Top 5 poses written to {args.docked_output}.\n')
    f.write(f'Minimized pose written to {args.minimized_output}.\n')

print(f"Docking completed for {args.receptor_file}")