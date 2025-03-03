input_file = "dragon_radii_aligned.aln"
output_file = "extracted_target.aln"

# Läs in alla icke-tomma rader från input-filen
with open(input_file, "r") as infile:
    sequences = [line.strip() for line in infile if line.strip()]

# Kontrollera att det finns minst en sekvens
if not sequences:
    raise ValueError("Ingen sekvens hittades i filen.")

# Extrahera den första sekvensen (target-sekvensen)
target_sequence = sequences[0]

# Skriv target-sekvensen till en ny fil
with open(output_file, "w") as outfile:
    outfile.write(target_sequence + "\n")

print(f"Target-sekvensen har sparats i {output_file}")
