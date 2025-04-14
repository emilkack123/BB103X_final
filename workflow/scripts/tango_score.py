#!/usr/bin/env python3

import argparse
import subprocess
from Bio import SeqIO
import pandas as pd
import tempfile
import os

def run_tango(seq_id, sequence, tango_path):
    # TANGO input format:
    # >id temperature pH ionic_strength threshold constant
    header = f">{seq_id} 298 7.4 0.02 0.1 1.0"
    sequence = sequence.upper()

    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".tango") as temp_file:
        temp_file.write(f"{header}\n{sequence}\n")
        temp_path = temp_file.name

    result = subprocess.run([tango_path, temp_path], capture_output=True, text=True)

    os.remove(temp_path)

    # Print for debugging
    print(f"\n--- Output for {seq_id} ---")
    print(result.stdout)
    print("---------------------------\n")

    # Parse aggregation score (customize this depending on actual output)
    score = None
    for line in result.stdout.splitlines():
        if "AGGREGATION" in line.upper():
            try:
                score = float(line.split()[-1])
                break
            except:
                continue

    return score


def main():
    parser = argparse.ArgumentParser(description="Run TANGO on sequences and save aggregation scores.")
    parser.add_argument("--input_fasta", required=True, help="Path to input FASTA file")
    parser.add_argument("--output_csv", required=True, help="Path to output CSV file")
    parser.add_argument("--tango_path", required=True, help="Path to tango binary")
    args = parser.parse_args()

    results = []
    for record in SeqIO.parse(args.input_fasta, "fasta"):
        seq_id = record.id
        sequence = str(record.seq)
        score = run_tango(seq_id, sequence, args.tango_path)
        results.append((seq_id, score))

    df = pd.DataFrame(results, columns=["sequence_id", "tango_score"])
    df.to_csv(args.output_csv, index=False)


if __name__ == "__main__":
    main()
