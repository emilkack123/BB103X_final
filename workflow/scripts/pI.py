import argparse
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils import IsoelectricPoint

def parse_fasta(fasta_file):
    """Parses a FASTA file and extracts sequences into a DataFrame."""
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append({"ID": record.id, "Sequence": str(record.seq)})
    return pd.DataFrame(sequences)

def calculate_pI(sequence):
    """Calculates isoelectric point (pI) of a protein sequence."""
    try:
        analyser = IsoelectricPoint.IsoelectricPoint(sequence)
        return analyser.pi()
    except:
        return None  # Handle invalid sequences

def main():
    parser = argparse.ArgumentParser(description="Compute isoelectric points (pI) for protein sequences.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTA file.")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file.")
    args = parser.parse_args()
    
    df = parse_fasta(args.input)
    df["pI"] = df["Sequence"].apply(calculate_pI)
    
    df.to_csv(args.output, index=False)
    print("\n✅ Computed pI values saved to:", args.output)
    print(df.drop(columns=["Sequence"]).head(10))  # Print top 10 rows

if __name__ == "__main__":
    main()
