import argparse
from collections import OrderedDict
from Bio import SeqIO
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("fasta", help="Original input FASTA file")
    parser.add_argument("iupred_output", help="Raw IUPred output (multi-sequence)")
    parser.add_argument("output_csv", help="Parsed disorder summary CSV")
    args = parser.parse_args()

    # 1. Read the sequence lengths and IDs
    seq_lengths = OrderedDict()
    for record in SeqIO.parse(args.fasta, "fasta"):
        seq_lengths[record.id] = len(record.seq)

    # 2. Read all relevant lines from IUPred output
    with open(args.iupred_output) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    idx = 0
    rows = []
    for seq_id, length in seq_lengths.items():
        scores = []
        for i in range(idx, idx + length):
            try:
                score = float(lines[i].split()[2])
                scores.append(score)
            except Exception:
                continue

        if not scores:
            continue

        disordered = [s for s in scores if s > 0.5]
        percent_disorder = len(disordered) / len(scores)
        disorder_segments = sum(
            1 for i in range(1, len(scores))
            if scores[i] > 0.5 and scores[i-1] <= 0.5
        )

        rows.append({
            "id": seq_id,
            "percent_disorder": percent_disorder,
            "num_disorder_segments": disorder_segments
        })
        idx += length

    df = pd.DataFrame(rows)
    df.to_csv(args.output_csv, index=False)

if __name__ == "__main__":
    main()
