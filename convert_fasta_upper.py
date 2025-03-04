#!/usr/bin/env python3
import sys

def convert_fasta_to_upper(input_file, output_file):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                outfile.write(line.upper())
        print(f"Conversion complete. Uppercase FASTA saved to {output_file}")
    except Exception as e:
        print(f"Error processing file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python convert_fasta_upper.py <input_fasta_file> <output_fasta_file>")
        sys.exit(1)
    
    input_fasta = sys.argv[1]
    output_fasta = sys.argv[2]
    convert_fasta_to_upper(input_fasta, output_fasta)
