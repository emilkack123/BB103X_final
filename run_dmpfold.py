#!/usr/bin/env python3
import subprocess

def run_dmpfold_for_sequence(seq, index):
    # Namnge filerna
    aln_filename = f"target_{index}.aln"
    pdb_filename = f"model_{index}.pdb"
    
    # Skriv sekvensen till en egen aln-fil
    with open(aln_filename, "w") as f:
        f.write(seq + "\n")
    
    print(f"Kör dmpfold på {aln_filename}...")
    
    # Kör dmpfold via subprocess
    result = subprocess.run(["dmpfold", "-i", aln_filename],
                            capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"Fel vid körning av dmpfold på {aln_filename}:")
        print(result.stderr)
    else:
        # Spara dmpfold-utdata i en pdb-fil
        with open(pdb_filename, "w") as f:
            f.write(result.stdout)
        print(f"Modell sparad i {pdb_filename}")

def main():
    input_file = "test.aln"
    # Läs in varje icke-tom rad (antag att varje rad är en korrekt formaterad sekvens)
    with open(input_file, "r") as f:
        sequences = [line.strip() for line in f if line.strip()]
    
    # Kör dmpfold för varje sekvens
    for idx, seq in enumerate(sequences, start=1):
        run_dmpfold_for_sequence(seq, idx)

if __name__ == "__main__":
    main()
