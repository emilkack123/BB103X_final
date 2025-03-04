#!/usr/bin/env python3
import subprocess
import os

def run_dmpfold_for_sequence(seq, index):
    # Name the files
    aln_filename = os.path.join("z2_targets", f"target_{index}.aln") 
    pdb_filename = os.path.join("z3_models", f"model_{index}.pdb")
    
    # Write the sequence to its own aln file
    with open(aln_filename, "w") as f:
        f.write(seq + "\n")
    
    print(f"Running dmpfold on {aln_filename}...")
    
    # Run dmpfold via subprocess
    result = subprocess.run(["dmpfold", "-i", aln_filename],
                            capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Error running dmpfold on {aln_filename}:")
        print(result.stderr)
    else:
        # Save dmpfold output to a pdb file
        with open(pdb_filename, "w") as f:
            f.write(result.stdout)
        print(f"Model saved in {pdb_filename}")

def main():
    input_file = "z1_resources/test.aln"
    # Read in each non-empty line (assume each line is a properly formatted sequence)
    with open(input_file, "r") as f:
        sequences = [line.strip() for line in f if line.strip()]
    
    # Run dmpfold for each sequence
    for idx, seq in enumerate(sequences, start=1):
        run_dmpfold_for_sequence(seq, idx)

if __name__ == "__main__":
    main()
