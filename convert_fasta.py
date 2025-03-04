from Bio import SeqIO
import re

input_file = "dragon_radii_updated.fasta"
output_file = "dragon_radii_aligned.aln"

with open(output_file, "w") as out_handle:
    for record in SeqIO.parse(input_file, "fasta"):
        # Convert the sequence to a string
        seq_str = str(record.seq).strip()
        # Remove lowercase letters (which removes any insertion letters)
        seq_str = re.sub(r'[a-z]', '', seq_str)
        # If it is the first sequence and you want to remove any gaps ('-'),
        # you can uncomment the following line.
        # if out_handle.tell() == 0:
        #     seq_str = seq_str.replace("-", "")
        # Write the sequence on one line
        out_handle.write(seq_str + "\n")

print(f"Converted file saved as {output_file}")
