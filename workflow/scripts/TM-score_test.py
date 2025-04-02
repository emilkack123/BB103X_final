import os
import csv
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Calculate TM-scores for PDB files and save results in CSV")
parser.add_argument('--pdb_folder', type=str, required=True, help="Path to the directory containing PDB files")
parser.add_argument('--reference_pdb', type=str, required=True, help="Path to the reference PDB file")
parser.add_argument('--output_csv', type=str, required=True, help="Path to the output CSV file")
parser.add_argument('--fasta_file', type=str, required=True, help="Path to the FASTA file with sequence IDs")

args = parser.parse_args()

# Get input arguments
pdb_folder = args.pdb_folder
reference_pdb = args.reference_pdb
output_csv = args.output_csv
fasta_file = args.fasta_file

# Specify the full path to the TMscore executable
tm_score_path = "/home/moa/BB103X_final/TMscore"

# Step 1: Extract sequence IDs from FASTA file (in order)
def read_fasta_ids(fasta_path):
    fasta_ids = []
    with open(fasta_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                fasta_id = line.split()[0].lstrip('>')  # Extract sequence ID
                fasta_ids.append(fasta_id.strip())  # Store it in order
    return fasta_ids

sequence_ids = read_fasta_ids(fasta_file)  # Read sequence IDs from gen.fa

# Step 2: Get PDB files in the specified directory
pdb_files = sorted([f for f in os.listdir(pdb_folder) if f.endswith('.pdb')])

# Step 3: Ensure correct mapping between sequence IDs and PDB files
if len(sequence_ids) != len(pdb_files):
    print("Warning: Number of sequences in gen.fa does not match number of PDB files.")
    exit(1)  # Exit if there's a mismatch

# Create a mapping: {model_gen_seq1.pdb → first sequence ID, model_gen_seq2.pdb → second, etc.}
pdb_to_seq_id = {pdb_files[i]: sequence_ids[i] for i in range(len(pdb_files))}

# Step 4: Open the CSV file for writing results
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['Sequence ID', 'TM-score']  # Updated column names
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Step 5: Loop through each PDB file and compute TM-score
    for pdb_file in pdb_files:
        pdb_path = os.path.join(pdb_folder, pdb_file)  # Get full path to PDB file
        seq_id = pdb_to_seq_id.get(pdb_file, "Unknown")  # Get corresponding sequence ID

        # Run TM-score via command line and capture the output
        output = os.popen(f"{tm_score_path} {pdb_path} {reference_pdb}").read()

        # Debugging: Print the full output of TMscore for inspection
        print(f"Output for {pdb_file}:\n{output}\n")

        # Extract the TM-score from the output
        tm_score = None
        for line in output.split("\n"):
            if "TM-score" in line and "normalized" not in line:
                if '=' in line:
                    tm_score = line.split('=')[1].strip()  # Extract TM-score
                    break  # Stop looping once found

        # If TM-score was found, write it to the CSV file
        if tm_score:
            writer.writerow({'Sequence ID': seq_id, 'TM-score': tm_score})
            print(f"TM-score for {seq_id} written to CSV")
        else:
            print(f"TM-score not found for {seq_id}")

print(f"TM-score results have been written to {output_csv}")
