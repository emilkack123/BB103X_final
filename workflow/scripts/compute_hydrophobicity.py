import argparse
import pandas as pd
from Bio import SeqIO
from Bio.SeqUtils.ProtParam import ProteinAnalysis

def parse_fasta(fasta_file):
    """Parses a FASTA file and extracts sequences into a DataFrame."""
    sequences = []
    for record in SeqIO.parse(fasta_file, "fasta"):
        sequences.append({"ID": record.id, "Sequence": str(record.seq)})
    return pd.DataFrame(sequences)

def calculate_gravy(sequence):
    """Calculates the GRAVY hydrophobicity score."""
    try:
        analysis = ProteinAnalysis(sequence)
        return analysis.gravy()
    except:
        return None  # Handle errors

def main():
    parser = argparse.ArgumentParser(description="Compute hydrophobicity (GRAVY) for protein sequences.")
    parser.add_argument("-i", "--input", required=True, help="Input FASTA file.")
    parser.add_argument("-o", "--output", required=True, help="Output CSV file.")
    args = parser.parse_args()
    
    df = parse_fasta(args.input)
    df["Hydrophobicity"] = df["Sequence"].apply(calculate_gravy)
    
    df.to_csv(args.output, index=False)
    print("\n✅ Computed Hydrophobicity values saved to:", args.output)
    print(df.drop(columns=["Sequence"]).head(10))  # Print top 10 rows

if __name__ == "__main__":
    main()
