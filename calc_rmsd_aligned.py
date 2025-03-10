#!/usr/bin/env python3
from Bio import pairwise2
from Bio.PDB import PDBParser, PPBuilder, Superimposer
import sys

def get_sequence_and_ca_atoms(structure):
    """
    Extraherar den sammansatta sekvensen och en lista med motsvarande Cα-atomer
    från alla polypeptidkedjor i strukturen.
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
    Utför en global alignment av de två sekvenserna och extraherar de Cα-atomer
    som motsvarar gemensamma (icke-gap) positioner i alignmenten.
    """
    # Använd globalxx (matchar identiska tecken, utan gapstraff)
    alignments = pairwise2.align.globalxx(seq1, seq2)
    best_alignment = alignments[0]
    aligned_seq1, aligned_seq2, score, start, end = best_alignment

    common_atoms1 = []
    common_atoms2 = []
    idx1 = 0
    idx2 = 0
    # Gå igenom de alignade sekvenserna position för position.
    for a1, a2 in zip(aligned_seq1, aligned_seq2):
        if a1 != "-" and a2 != "-":
            # Båda positionerna motsvarar ett riktigt residu
            common_atoms1.append(ca_atoms1[idx1])
            common_atoms2.append(ca_atoms2[idx2])
            idx1 += 1
            idx2 += 1
        elif a1 != "-" and a2 == "-":
            idx1 += 1
        elif a1 == "-" and a2 != "-":
            idx2 += 1
        else:
            # Om båda är gap, vilket sällan sker
            continue
    return common_atoms1, common_atoms2

def main(pdb_file1, pdb_file2):
    parser = PDBParser(QUIET=True)
    structure1 = parser.get_structure("struct1", pdb_file1)
    structure2 = parser.get_structure("struct2", pdb_file2)

    # Hämta sekvens och Cα-atomer för båda strukturerna
    seq1, ca_atoms1 = get_sequence_and_ca_atoms(structure1)
    seq2, ca_atoms2 = get_sequence_and_ca_atoms(structure2)

    # Utför alignment och extrahera gemensamma Cα-atomer
    common_atoms1, common_atoms2 = align_and_extract(seq1, seq2, ca_atoms1, ca_atoms2)

    if len(common_atoms1) == 0 or len(common_atoms1) != len(common_atoms2):
        sys.exit("Fel: Kunde inte identifiera gemensamma Cα-atomer mellan strukturerna.")

    # Superponera de gemensamma atomerna och beräkna RMSD
    super_imposer = Superimposer()
    super_imposer.set_atoms(common_atoms1, common_atoms2)
    print("RMSD:", super_imposer.rms)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Användning: python calc_rmsd_aligned.py struktur1.pdb struktur2.pdb")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
