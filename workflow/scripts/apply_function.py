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
            raise ValueError(f"Column '{key}' not found in {file}")
        # Use the user-provided data column name for the metric value
        data_col = data_cols[i]
        if data_col not in df.columns:
            raise ValueError(f"Data column '{data_col}' not found in {file}")
        # Determine the new output column name for the metric
        metric_name = metrics[i] if metrics else file.split('.')[0]
        # Keep only the key and data columns, renaming the key to the common key and the data column to metric_name
        df = df[[key, data_col]].rename(columns={key: common_key, data_col: metric_name})
        if merged_df is None:
            merged_df = df
        else:
            merged_df = pd.merge(merged_df, df, on=common_key, how='outer')
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
                        help="List of metric (data) column names for each file (in the same order as --files).")
    parser.add_argument('--metrics', nargs='+', required=False,
                        help="List of output column names for each metric. If not provided, file basenames are used.")
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
