#!/usr/bin/env python3
from Bio.PDB import PDBParser, Superimposer
import sys

def get_ca_atoms(structure):
    """Extrahera Cα-atomer från alla modeller, kedjor och rester i en struktur."""
    ca_atoms = []
    for model in structure:
        for chain in model:
            for residue in chain:
                # Säkerställ att resten har en CA-atom (det kan finnas vatten eller andra molekyler)
                if "CA" in residue:
                    ca_atoms.append(residue["CA"])
    return ca_atoms

def main(pdb_file1, pdb_file2):
    parser = PDBParser(QUIET=True)
    # Läs in strukturerna från filerna
    structure1 = parser.get_structure("struct1", pdb_file1)
    structure2 = parser.get_structure("struct2", pdb_file2)
    
    # Hämta listor med Cα-atomer från båda strukturerna
    ca_atoms1 = get_ca_atoms(structure1)
    ca_atoms2 = get_ca_atoms(structure2)
    
    # Kontrollera att antalet Cα-atomer är lika
    if len(ca_atoms1) != len(ca_atoms2):
        sys.exit("Fel: Strukturerna har olika antal Cα-atomer. Kontrollera att de är parvis jämförbara.")
    
    # Utför superpositionen och beräkna RMSD
    super_imposer = Superimposer()
    super_imposer.set_atoms(ca_atoms1, ca_atoms2)
    
    print("RMSD:", super_imposer.rms)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Användning: python calc_rmsd.py struktur1.pdb struktur2.pdb")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
