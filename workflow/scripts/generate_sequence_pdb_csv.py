#!/usr/bin/env python3
import os
import csv
from Bio import SeqIO

fasta_path = "resources/rubisco_sequences/dragon_radii_updated_704.fasta"
pdb_folder = "results/dragon_radii_updated_some_pdb_files"
output_csv = "sequences_with_pdbs.csv"

pdb_files = [fn for fn in os.listdir(pdb_folder) if fn.lower().endswith(".pdb")]
pdb_basenames = {os.path.splitext(fn)[0]: fn for fn in pdb_files}

with open(output_csv, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["seq_id", "sequence", "pdb_file"])
    for record in SeqIO.parse(fasta_path, "fasta"):
        seq_id = record.id
        seq = str(record.seq)
        pdb_fn = pdb_basenames.get(seq_id, "")
        writer.writerow([seq_id, seq, pdb_fn])

print(f"Wrote {output_csv} with {len(pdb_files)} PDB files referenced.")
