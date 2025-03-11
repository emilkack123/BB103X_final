import py3Dmol
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

view = py3Dmol.view()
view.removeAllModels()
view.setViewStyle({'style':'outline','color':'black','width':0.1})

view.addModel(open('/home/moa/BB103X_final/enzyme.pdbqt','r').read(),format='pdbqt')
Prot=view.getModel()
Prot.setStyle({
    'cartoon':{'arrows':True, 
               'helixes':True, 
               #'tubes':True
               'style':'oval', 
               'color':'spectrum'}})
view.addSurface(py3Dmol.VDW,{'opacity':0.6,'color':'white'})
view.addBox({
    'center':{'x':cx,'y':cy,'z':cz},
    'dimensions': {'w':bx,'h':by,'d':bz}, 
    'color': 'magenta', 
    'opacity':0.5})
view.addModel(open('/home/moa/BB103X_final/results/docking/co2.mol','r').read(),format='mol')
ref_m = view.getModel()
ref_m.setStyle({},{'stick':{'colorscheme':'greenCarbon','radius':0.2}})

view.zoomTo()
view.show()