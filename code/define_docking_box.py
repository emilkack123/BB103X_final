from vina import Vina

cx = 50  # Center x-coordinate
cy = 50  # Center y-coordinate
cz = 50  # Center z-coordinate
bx = 20  # Box size in x direction (in Å)
by = 20  # Box size in y direction (in Å)
bz = 20  # Box size in z direction (in Å)

v = Vina(sf_name='vina')

v.set_receptor('input_rubisco.pdbqt')
v.set_ligand_from_file('input_co2.pdbqt')
v.compute_vina_maps(center=[cx, cy, cz], box_size=[bx, by, bz])

