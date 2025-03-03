from Bio import SeqIO
import re

input_file = "dragon_radii_updated.fasta"
output_file = "dragon_radii_aligned.aln"

with open(output_file, "w") as out_handle:
    for record in SeqIO.parse(input_file, "fasta"):
        # Konvertera sekvensen till en sträng
        seq_str = str(record.seq).strip()
        # Ta bort små bokstäver (vilket tar bort eventuella insertionsbokstäver)
        seq_str = re.sub(r'[a-z]', '', seq_str)
        # Om det är den första sekvensen och du vill ta bort eventuella gap ('-'),
        # kan du avkommentera nästa rad.
        # if out_handle.tell() == 0:
        #     seq_str = seq_str.replace("-", "")
        # Skriv ut sekvensen på en rad
        out_handle.write(seq_str + "\n")

print(f"Konverterad fil sparad som {output_file}")
