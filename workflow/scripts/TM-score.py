import os
import csv
import argparse

# Set up argument parsing
parser = argparse.ArgumentParser(description="Calculate TM-scores for PDB files and save results in CSV")
parser.add_argument('--pdb_folder', type=str, required=True, help="Path to the directory containing PDB files")
parser.add_argument('--reference_pdb', type=str, required=True, help="Path to the reference PDB file")
parser.add_argument('--output_csv', type=str, required=True, help="Path to the output CSV file")

args = parser.parse_args()

# Get PDB files in the specified directory
pdb_folder = args.pdb_folder
reference_pdb = args.reference_pdb
output_csv = args.output_csv

# Specify the full path to the TMscore executable
tm_score_path = "/home/moa/BB103X_final/TMscore"

# Get a list of all PDB files in the directory
pdb_files = [f for f in os.listdir(pdb_folder) if f.endswith('.pdb')]

# Open the CSV file for writing the results
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ['PDB File', 'TM-score']  # Column headers
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    # Loop through each PDB file in the folder
    for pdb_file in pdb_files:
        pdb_path = os.path.join(pdb_folder, pdb_file)  # Get full path to PDB file
        
        # Run TM-score via command line and capture the output
        output = os.popen(f"{tm_score_path} {pdb_path} {reference_pdb}").read()

        # Debugging: Print the full output of TMscore for inspection
        print(f"Output for {pdb_file}:\n{output}\n")

        # Extract the TM-score from the output
        tm_score = None
        for line in output.split("\n"):
            if "TM-score" in line and "normalized" not in line:
                # Check if the line contains '=' before attempting to split
                if '=' in line:
                    tm_score = line.split('=')[1].strip()  # Extract the TM-score value
                    break  # Stop looping once the TM-score is found

        # If TM-score was found, write it to the CSV file
        if tm_score:
            writer.writerow({'PDB File': pdb_file, 'TM-score': tm_score})
            print(f"TM-score for {pdb_file} written to CSV")
        else:
            print(f"TM-score not found for {pdb_file}")

print(f"TM-score results have been written to {output_csv}")
