#!/usr/bin/env python

import argparse
import pandas as pd
from Bio import SeqIO

def fasta_to_csv(fasta_file, csv_file):
    """Converts a FASTA file to a CSV file."""
    # Read sequences from FASTA file using Biopython's SeqIO
    records = list(SeqIO.parse(fasta_file, "fasta"))
    
    # Create a DataFrame from the FASTA records
    data = {
        "id": [record.id for record in records],
        "description": [record.description for record in records],
        "sequence": [str(record.seq) for record in records]
    }
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(data)
    
    # Save DataFrame to CSV
    df.to_csv(csv_file, index=False)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Convert a FASTA file to CSV.")
    parser.add_argument("fasta_file", help="Input FASTA file")
    parser.add_argument("csv_file", help="Output CSV file")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Convert the FASTA to CSV
    fasta_to_csv(args.fasta_file, args.csv_file)

if __name__ == "__main__":
    main()
