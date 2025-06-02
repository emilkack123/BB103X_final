import argparse
from Bio import SeqIO
import pandas as pd
from Bio.SeqUtils.ProtParam import ProteinAnalysis

def compute_hydrophobicity(gen_fasta, nat_fasta, output_csv):
    data = []

    for file_path, origin in [(gen_fasta, "Generated"), (nat_fasta, "Natural")]:
        for record in SeqIO.parse(file_path, "fasta"):
            seq = str(record.seq)
            if 'X' in seq.upper():
                print(f"Skipping {record.id} due to unknown amino acids.")
                continue
            analysed_seq = ProteinAnalysis(seq)
            hydrophobicity = analysed_seq.gravy()
            data.append({"ID": record.id, "Hydrophobicity": hydrophobicity, "Origin": origin})

    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("gen_fasta", help="Fasta file with generated sequences")
    parser.add_argument("nat_fasta", help="Fasta file with natural sequences")
    parser.add_argument("output_csv", help="Output CSV file")
    args = parser.parse_args()

    compute_hydrophobicity(args.gen_fasta, args.nat_fasta, args.output_csv)
