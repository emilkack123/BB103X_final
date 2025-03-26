import openbabel

# Initialize Open Babel's OBConversion object
obConversion = openbabel.OBConversion()

# Set input and output formats (SDF -> PDBQT)
obConversion.SetInAndOutFormats("sdf", "pdbqt")

# Create an OBMol object to hold the molecule
mol = openbabel.OBMol()

# Read the SDF file (replace "input_file.sdf" with your actual SDF file path)
obConversion.ReadFile(mol, "resources/docking/co2.sdf") 

# Add hydrogens to the molecule (if not already present)
mol.AddHydrogens()

# Optionally, print out some information about the molecule
print(f"Number of atoms: {mol.NumAtoms()}")
print(f"Number of bonds: {mol.NumBonds()}")
print(f"Number of residues: {mol.NumResidues()}")

# Add the "h" option for adding hydrogens in the output (if needed)
obConversion.AddOption("h")

# Write the file in PDBQT format
obConversion.WriteFile(mol, 'results/co2.pdbqt')
