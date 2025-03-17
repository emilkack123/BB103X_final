#!/usr/bin/env python3
import argparse
import subprocess
import os

def run_dmpfold_for_sequence(seq, index, target_dir, model_dir):
    # Konstruera filnamn med angivna kataloger
    aln_filename = os.path.join(target_dir, f"target_{index}.aln")
    pdb_filename = os.path.join(model_dir, f"model_{index}.pdb")
    
    # Skriv sekvensen till sin ALN-fil
    with open(aln_filename, "w") as f:
        f.write(seq + "\n")
    
    print(f"Running dmpfold on {aln_filename}...")
    
    # Kör dmpfold med flaggorna -n 0 och -m 0
    result = subprocess.run(
        ["dmpfold", "-i", aln_filename, "-n", "0", "-m", "0"],
        capture_output=True, text=True
    )
    
    if result.returncode != 0:
        print(f"Error running dmpfold on {aln_filename}:")
        print(result.stderr)
    else:
        # Spara dmpfold-output till en PDB-fil
        with open(pdb_filename, "w") as f:
            f.write(result.stdout)
        print(f"Model saved in {pdb_filename}")

def main():
    parser = argparse.ArgumentParser(
        description="Run dmpfold on each sequence in an ALN file and save the outputs."
    )
    parser.add_argument("input_file", help="Path to the input ALN file containing sequences")
    parser.add_argument(
        "--target_dir", default="z4_targets_natural",
        help="Directory to store target ALN files (default: z4_targets_natural)"
    )
    parser.add_argument(
        "--model_dir", default="z5_models_natural",
        help="Directory to store model PDB files (default: z5_models_natural)"
    )
    
    args = parser.parse_args()
    
    # Skapa utdata-kataloger om de inte finns
    os.makedirs(args.target_dir, exist_ok=True)
    os.makedirs(args.model_dir, exist_ok=True)
    
    # Läs in varje icke-tom rad från indatafilen (varje rad ska vara en korrekt formaterad sekvens)
    try:
        with open(args.input_file, "r") as f:
            sequences = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"Error reading {args.input_file}: {e}")
        exit(1)
    
    # Kör dmpfold för varje sekvens
    for idx, seq in enumerate(sequences, start=1):
        run_dmpfold_for_sequence(seq, idx, args.target_dir, args.model_dir)

if __name__ == "__main__":
    main()
