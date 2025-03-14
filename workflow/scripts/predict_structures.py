from esm import FoldTrajPredictor, pretrained
from Bio import SeqIO
import os

# Load ESMFold model
model = pretrained.esmfold_v1()

# Input and output paths
input_fasta = "resources/cleaned.fasta"
output_dir = "results/structures/"

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Process sequences
for record in SeqIO.parse(input_fasta, "fasta"):
    sequence_id = record.id
    sequence = str(record.seq)

    # Predict structure using ESMFold
    output = model.infer(sequence)

    # Save structure to PDB file
    output_path = os.path.join(output_dir, f"{sequence_id}.pdb")
    with open(output_path, "w") as f:
        f.write(str(output))

    print(f"Saved structure for {sequence_id} at {output_path}")
