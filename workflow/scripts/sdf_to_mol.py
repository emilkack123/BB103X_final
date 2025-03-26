import openbabel

# Initialize Open Babel's OBConversion object
obConversion = openbabel.OBConversion()

# Set input and output formats (SDF -> MOL)
obConversion.SetInAndOutFormats("sdf", "mol")

# Create an OBMol object to hold the molecule
mol = openbabel.OBMol()

# Read the SDF file
input_sdf = "/home/moa/BB103X_final/resources/docking/co2.sdf"
output_mol = "/home/moa/BB103X_final/results/docking/co2.mol"

if obConversion.ReadFile(mol, input_sdf):  # Check if file is successfully read
    # Write the file in MOL format
    obConversion.WriteFile(mol, output_mol)
    print(f"Conversion successful: {input_sdf} → {output_mol}")
else:
    print("Error: Could not read the SDF file.")
