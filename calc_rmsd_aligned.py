#!/usr/bin/env python3
from Bio import pairwise2
from Bio.PDB import PDBParser, PPBuilder, Superimposer
import sys

def get_sequence_and_ca_atoms(structure):
    """
    Extracts the combined sequence and a list of corresponding Cα atoms
    from all polypeptide chains in the structure.
    """
    ppb = PPBuilder()
    sequence = ""
    ca_atoms = []
    for pp in ppb.build_peptides(structure):
        sequence += str(pp.get_sequence())
        for residue in pp:
            if "CA" in residue:
                ca_atoms.append(residue["CA"])
    return sequence, ca_atoms

def align_and_extract(seq1, seq2, ca_atoms1, ca_atoms2):
    """
    Performs a global alignment of the two sequences and extracts the Cα atoms
    corresponding to common (non-gap) positions in the alignment.
    """
    # Use globalxx (matches identical characters without gap penalties)
    alignments = pairwise2.align.globalxx(seq1, seq2)
    best_alignment = alignments[0]
    aligned_seq1, aligned_seq2, score, start, end = best_alignment

    common_atoms1 = []
    common_atoms2 = []
    idx1 = 0
    idx2 = 0
    # Iterate through the aligned sequences position by position.
    for a1, a2 in zip(aligned_seq1, aligned_seq2):
        if a1 != "-" and a2 != "-":
            # Both positions correspond to a real residue
            common_atoms1.append(ca_atoms1[idx1])
            common_atoms2.append(ca_atoms2[idx2])
            idx1 += 1
            idx2 += 1
        elif a1 != "-" and a2 == "-":
            idx1 += 1
        elif a1 == "-" and a2 != "-":
            idx2 += 1
        else:
            # If both are gaps, which rarely happens
            continue
    return common_atoms1, common_atoms2

def main(pdb_file1, pdb_file2):
    parser = PDBParser(QUIET=True)
    structure1 = parser.get_structure("struct1", pdb_file1)
    structure2 = parser.get_structure("struct2", pdb_file2)

    # Retrieve the sequence and Cα atoms for both structures
    seq1, ca_atoms1 = get_sequence_and_ca_atoms(structure1)
    seq2, ca_atoms2 = get_sequence_and_ca_atoms(structure2)

    # Perform alignment and extract common Cα atoms
    common_atoms1, common_atoms2 = align_and_extract(seq1, seq2, ca_atoms1, ca_atoms2)

    if len(common_atoms1) == 0 or len(common_atoms1) != len(common_atoms2):
        sys.exit("Error: Could not identify common Cα atoms between the structures.")

    # Superimpose the common atoms and calculate RMSD
    super_imposer = Superimposer()
    super_imposer.set_atoms(common_atoms1, common_atoms2)
    print("RMSD:", super_imposer.rms)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python calc_rmsd_aligned.py structure1.pdb structure2.pdb")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
