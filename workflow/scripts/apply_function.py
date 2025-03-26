#!/usr/bin/env python3
import pandas as pd
import argparse

def merge_csv_files(files, keys, data_cols, metrics, common_key="ID"):
    if len(files) != len(keys):
        raise ValueError("The number of files and key column names must match.")
    if data_cols and (len(data_cols) != len(files)):
        raise ValueError("If data column names are provided, their number must match the number of files.")
    if metrics and (len(metrics) != len(files)):
        raise ValueError("If metric names are provided, their number must match the number of files.")
    
    merged_df = None
    for i, file in enumerate(files):
        key = keys[i]
        df = pd.read_csv(file)
        if key not in df.columns:
            raise ValueError(f"Key column '{key}' not found in {file}")
        # Allow comma-separated list for data columns
        data_cols_list = [col.strip() for col in data_cols[i].split(',')]
        for col in data_cols_list:
            if col not in df.columns:
                raise ValueError(f"Data column '{col}' not found in {file}")
        # Process metric names for renaming: allow comma-separated names too
        if metrics:
            metric_names = [x.strip() for x in metrics[i].split(',')]
            if len(metric_names) != len(data_cols_list):
                raise ValueError(f"In file {file}, number of metric names does not match number of data columns.")
        else:
            metric_names = data_cols_list
        
        # Create a dataframe with the key and the desired data columns, and rename them
        selected_df = df[[key] + data_cols_list].copy()
        rename_dict = {key: common_key}
        for orig, new in zip(data_cols_list, metric_names):
            rename_dict[orig] = new
        selected_df = selected_df.rename(columns=rename_dict)
        
        if merged_df is None:
            merged_df = selected_df
        else:
            merged_df = pd.merge(merged_df, selected_df, on=common_key, how='outer')
    return merged_df

def parse_args():
    parser = argparse.ArgumentParser(
        description="Merge metric CSV files with different key and data columns into a single CSV."
    )
    parser.add_argument('--files', nargs='+', required=True,
                        help="List of CSV files to merge.")
    parser.add_argument('--keys', nargs='+', required=True,
                        help="List of key column names for each file (in the same order as --files).")
    parser.add_argument('--data_cols', nargs='+', required=True,
                        help="List of metric (data) column names for each file. Use a comma-separated list for multiple columns.")
    parser.add_argument('--metrics', nargs='+', required=False,
                        help="List of output column names for each metric column. Use a comma-separated list for multiple columns. If not provided, original column names are used.")
    parser.add_argument('--common_key', default="ID",
                        help="Name for the common key column in the merged output (default: 'ID').")
    parser.add_argument('--output', required=True,
                        help="Output CSV file name.")
    return parser.parse_args()

def main():
    args = parse_args()
    merged_df = merge_csv_files(args.files, args.keys, args.data_cols, args.metrics, common_key=args.common_key)
    merged_df.to_csv(args.output, index=False)
    print(f"Merged CSV written to {args.output}")

if __name__ == '__main__':
    main()
