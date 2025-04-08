import argparse
import re
import pandas as pd
from collections import defaultdict

def parse_iupred(file_path):
    data = defaultdict(list)
    current_id = None

    with open(file_path) as f:
        for line in f:
            if line.startswith(">"):
                current_id = line.strip()[1:]
            elif re.match(r'^\d+\s+\w\s+[0-9.]+', line):
                _, _, score = line.strip().split()
                data[current_id].append(float(score))

    rows = []
    for seq_id, scores in data.items():
        disordered = [s for s in scores if s > 0.5]
        percent_disorder = len(disordered) / len(scores)
        disorder_regions = sum(
            1 for i in range(1, len(scores))
            if scores[i] > 0.5 and scores[i-1] <= 0.5
        )
        rows.append({
            "id": seq_id,
            "percent_disorder": percent_disorder,
            "num_disorder_segments": disorder_regions
        })

    return pd.DataFrame(rows)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="IUPred output .txt")
    parser.add_argument("output", help="CSV file to save results")
    args = parser.parse_args()

    df = parse_iupred(args.input)
    df.to_csv(args.output, index=False)

if __name__ == "__main__":
    main()
