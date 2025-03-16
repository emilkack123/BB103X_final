#!/usr/bin/env python3
import argparse
import subprocess
import os

def run_dmpfold_for_sequence(seq, index, target_dir, model_dir):
    # Construct file names using the specified directories
    aln_filename = os.path.join(target_dir, f"target_{index}.aln")
    pdb_filename = os.path.join(model_dir, f"model_{index}.pdb")
    
    # Write the sequence to its own ALN file
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
        # Save dmpfold output to a PDB file
        with open(pdb_filename, "w") as f:
            f.write(result.stdout)
        print(f"Model saved in {pdb_filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Run dmpfold on each sequence in an ALN file and save the outputs."
    )
    parser.add_argument("input_file", help="Path to the input ALN file containing sequences")
    parser.add_argument(
        "--target_dir", default="z2_targets_gen",
        help="Directory to store target ALN files (default: z2_targets_gen)"
    )
    parser.add_argument(
        "--model_dir", default="z3_models_gen",
        help="Directory to store model PDB files (default: z3_models_gen)"
    )
    
    args = parser.parse_args()
    
    # Ensure the output directories exist
    os.makedirs(args.target_dir, exist_ok=True)
    os.makedirs(args.model_dir, exist_ok=True)
    
    # Read in each non-empty line from the input file (each line is a properly formatted sequence)
    try:
        with open(args.input_file, "r") as f:
            sequences = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading {args.input_file}: {e}")
        exit(1)
    
    # Run dmpfold for each sequence
    for idx, seq in enumerate(sequences, start=1):
        run_dmpfold_for_sequence(seq, idx, args.target_dir, args.model_dir)

if __name__ == "__main__":
    main()
