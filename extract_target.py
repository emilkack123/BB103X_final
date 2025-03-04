input_file = "dragon_radii_aligned.aln"
output_file = "extracted_target.aln"

# Read all non-empty lines from the input file
with open(input_file, "r") as infile:
    sequences = [line.strip() for line in infile if line.strip()]

# Check that at least one sequence exists
if not sequences:
    raise ValueError("No sequence found in the file.")

# Extract the first sequence (the target sequence)
target_sequence = sequences[0]

# Write the target sequence to a new file
with open(output_file, "w") as outfile:
    outfile.write(target_sequence + "\n")

print(f"The target sequence has been saved in {output_file}")
