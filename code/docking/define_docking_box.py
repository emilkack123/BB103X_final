from vina import Vina

cx = 50  # Center x-coordinate
cy = 50  # Center y-coordinate
cz = 50  # Center z-coordinate
bx = 20  # Box size in x direction (in Å)
by = 20  # Box size in y direction (in Å)
bz = 20  # Box size in z direction (in Å)

v = Vina(sf_name='vina')

v.set_receptor('/home/moa/BB103X_final/enzyme.pdbqt')
v.set_ligand_from_file('/home/moa/BB103X_final/results/docking/co2.pdbqt')
v.compute_vina_maps(center=[cx, cy, cz], box_size=[bx, by, bz])

