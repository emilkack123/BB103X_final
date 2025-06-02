import argparse
from Bio import SeqIO
from Bio.SeqUtils import molecular_weight
import pandas as pd

def compute_metrics(gen_fasta, nat_fasta, output_csv):
    data = []

    for fasta_file, label in [(gen_fasta, "Generated"), (nat_fasta, "Natural")]:
        for record in SeqIO.parse(fasta_file, "fasta"):
            seq_str = str(record.seq).upper()
            if 'X' in seq_str:
                print(f"Skipping {record.id} due to unknown amino acids.")
                continue
            try:
                seq_length = len(record.seq)
                mol_weight = molecular_weight(record.seq, seq_type="protein")
                data.append([record.id, seq_length, mol_weight, label])
            except Exception as e:
                print(f"Error processing {record.id}: {e}")

    df = pd.DataFrame(data, columns=["Sequence_ID", "Sequence_Length", "Molecular_Weight", "Type"])
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute sequence length and molecular weight")
    parser.add_argument("gen_fasta", help="Path to generated FASTA file")
    parser.add_argument("nat_fasta", help="Path to natural FASTA file")
    parser.add_argument("output_csv", help="Path to output CSV file")

    args = parser.parse_args()
    compute_metrics(args.gen_fasta, args.nat_fasta, args.output_csv)
