#!/usr/bin/env python3
import argparse

def convert_fasta_to_upper(input_file, output_file):
    try:
        with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
            for line in infile:
                outfile.write(line.upper())
        print(f"Conversion complete. Uppercase FASTA saved to {output_file}")
    except Exception as e:
        print(f"Error processing file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Convert a FASTA file's content to uppercase.")
    parser.add_argument("input_fasta", help="Path to the input FASTA file")
    parser.add_argument("output_fasta", help="Path to the output FASTA file")
    args = parser.parse_args()

    convert_fasta_to_upper(args.input_fasta, args.output_fasta)

if __name__ == "__main__":
    main()
