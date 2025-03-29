#!/usr/bin/env python3

import argparse
import pandas as pd

def add_closest_column(dist_mat_file, input_csv_file, output_csv_file, sort=False):
    # Load the distance matrix
    dist_mat = pd.read_csv(dist_mat_file, index_col=0, header=None, skiprows=1, sep=r'\s+')
    dist_mat.index.name = None
    dist_mat.columns = dist_mat.index

    # Load the output CSV
    output_df = pd.read_csv(input_csv_file, index_col=0)

    # Get the quadrant of the distance matrix that contains the distances between generated and natural sequences
    gen_vs_nat_quadrant = dist_mat.loc[output_df[output_df['origin'] == 'generated'].index, output_df[output_df['origin'] == 'natural'].index]
    
    # Find the closest natural sequence for each generated sequence
    closest_sequences = gen_vs_nat_quadrant.idxmin(axis=1)
    distance_to_closest = gen_vs_nat_quadrant.min(axis=1)
    
    # Add the closest natural column to the output dataframe
    output_df['closest_natural'] = closest_sequences
    output_df['distance_to_closest'] = distance_to_closest
    
    # Sort by the distance_to_closest column if specified
    if sort:
        output_df = output_df.sort_values(by='distance_to_closest')

    # Save the updated dataframe to the output CSV
    output_df.to_csv(output_csv_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add closest sequence column to CSV.')
    parser.add_argument('dist_mat_file', help='Path to the distance matrix file.')
    parser.add_argument('input_csv_file', help='Path to the output CSV file.')
    parser.add_argument('output_csv_file', help='Path to the output CSV file.')
    parser.add_argument('--sort', action='store_true', help='Sort the output CSV by distance to closest sequence.')
    
    args = parser.parse_args()
    
    add_closest_column(args.dist_mat_file, args.input_csv_file, args.output_csv_file, sort=args.sort)
