#!/usr/bin/env python3
import argparse
import sys

def fasta_to_aln(fasta_file, aln_file):
    """
    Reads a FASTA file and writes an ALN file for DMPfold.
    - Lines starting with '>' are ignored.
    - Sequence lines for each record are concatenated.
    - The first sequence (target) is written without gap characters.
    """
    sequences = []
    current_seq = ""
    
    try:
        with open(fasta_file, "r") as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    continue  # skip empty lines
                if line.startswith(">"):
                    # Save previous sequence if it exists
                    if current_seq:
                        sequences.append(current_seq)
                        current_seq = ""
                    continue  # skip header lines
                else:
                    current_seq += line
            # Add the last sequence read
            if current_seq:
                sequences.append(current_seq)
    except Exception as e:
        print(f"Error reading {fasta_file}: {e}")
        sys.exit(1)
    
    if not sequences:
        print("No sequences found in the FASTA file.")
        sys.exit(1)
    
    # Ungap the target sequence (first sequence)
    sequences[0] = sequences[0].replace("-", "")
    
    try:
        with open(aln_file, "w") as fout:
            for seq in sequences:
                fout.write(seq + "\n")
        print(f"ALN file successfully written to: {aln_file}")
    except Exception as e:
        print(f"Error writing {aln_file}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Convert a FASTA file into an ALN file for DMPfold."
    )
    parser.add_argument("fasta_file", help="Path to the input FASTA file")
    parser.add_argument("aln_file", help="Path to the output ALN file")
    args = parser.parse_args()

    fasta_to_aln(args.fasta_file, args.aln_file)

if __name__ == "__main__":
    main()
