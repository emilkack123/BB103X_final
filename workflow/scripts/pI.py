import argparse
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis
import pandas as pd

def compute_pI(gen_fasta, nat_fasta, output_csv):
    data = []

    for fasta_file, label in [(gen_fasta, "Generated"), (nat_fasta, "Natural")]:
        for record in SeqIO.parse(fasta_file, "fasta"):
            try:
                seq = str(record.seq)
                analysed_seq = ProteinAnalysis(seq)
                pi = analysed_seq.isoelectric_point()
                data.append([record.id, pi, label])
            except Exception as e:
                print(f"Skipping {record.id} due to error: {e}")

    df = pd.DataFrame(data, columns=["Sequence_ID", "pI", "Type"])
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute isoelectric points (pI) for protein sequences")
    parser.add_argument("gen_fasta", help="Path to generated FASTA file")
    parser.add_argument("nat_fasta", help="Path to natural FASTA file")
    parser.add_argument("output_csv", help="Path to output CSV file")

    args = parser.parse_args()
    compute_pI(args.gen_fasta, args.nat_fasta, args.output_csv)
