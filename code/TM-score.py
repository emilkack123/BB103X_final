import os
import csv

# Path to the directory containing PDB files
pdb_folder = "/home/moa/BB103X_final/test_natural_structure"
# Path to the reference PDB file
reference_pdb = "/home/moa/BB103X_final/results/nat_structures/model_natural4.pdb"

# Define the output CSV file where TM-score results will be saved
output_csv = "/home/moa/BB103X_final/results/tm_score_results_test.csv"

# Get all PDB files in the directory (assuming files end with .pdb)
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
        output = os.popen(f"./TMscore {pdb_path} {reference_pdb}").read()

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

