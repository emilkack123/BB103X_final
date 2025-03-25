#!/usr/bin/env python3

import argparse
import pandas as pd

def determine_origin(sequence_id):
    if "." in sequence_id:
        return 'natural'
    else:
        return 'generated'

def add_origin_column(input_file, output_file):
    df = pd.read_csv(input_file)
    df['origin'] = df['id'].apply(determine_origin)
    df.to_csv(output_file, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add an Origin column to a CSV file containing amino acid sequences.')
    parser.add_argument('input_file', help='Path to the input CSV file')
    parser.add_argument('output_file', help='Path to the output CSV file')
    
    args = parser.parse_args()
    
    add_origin_column(args.input_file, args.output_file)