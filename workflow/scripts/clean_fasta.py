#!/usr/bin/env python3

import argparse
from Bio import SeqIO

# Set of valid amino acid characters
VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")

# Check if a sequence contains only valid amino acid characters
def is_valid_sequence(sequence):
    return all(char.upper() in VALID_AMINO_ACIDS for char in sequence)

# Clean a FASTA file by removing invalid sequences and converting sequences to uppercase
def clean_fasta(input_file, output_file, to_uppercase):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        for record in SeqIO.parse(infile, "fasta"):
            sequence = str(record.seq)
            if not is_valid_sequence(sequence):
                print(f"Invalid sequence found: {record.id}\n{sequence}")
            else:
                if to_uppercase:
                    sequence = sequence.upper()
                outfile.write(f">{record.id}\n{sequence}\n")

def main():
    parser = argparse.ArgumentParser(description="Clean FASTA files.")
    parser.add_argument("input_file", help="Input FASTA file")
    parser.add_argument("output_file", help="Output cleaned FASTA file")
    parser.add_argument("--to-uppercase", action="store_true", help="Convert sequences to uppercase")
    args = parser.parse_args()

    clean_fasta(args.input_file, args.output_file, args.to_uppercase)

if __name__ == "__main__":
    main()