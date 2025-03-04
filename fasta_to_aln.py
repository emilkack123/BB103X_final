#!/usr/bin/env python3
import sys

def fasta_to_aln(fasta_file, aln_file):
    """
    Reads a FASTA file and writes an ALN file for DMPfold.
    - Lines starting with '>' are ignored.
    - Sequence lines for each record are concatenated.
    - The first sequence (target) is written without gap characters.
    """
    sequences = []
    current_seq = ""
    
    try:
        with open(fasta_file, "r") as fin:
            for line in fin:
                line = line.strip()
                if not line:
                    continue  # skip empty lines
                if line.startswith(">"):
                    # save previous sequence if it exists
                    if current_seq:
                        sequences.append(current_seq)
                        current_seq = ""
                    # skip header lines
                    continue
                else:
                    current_seq += line
            # add the last sequence read
            if current_seq:
                sequences.append(current_seq)
    except Exception as e:
        print(f"Error reading {fasta_file}: {e}")
        sys.exit(1)
    
    if not sequences:
        print("No sequences found in the FASTA file.")
        sys.exit(1)
    
    # Ungap the target sequence (first sequence)
    sequences[0] = sequences[0].replace("-", "")
    
    try:
        with open(aln_file, "w") as fout:
            for seq in sequences:
                fout.write(seq + "\n")
        print(f"ALN file successfully written to: {aln_file}")
    except Exception as e:
        print(f"Error writing {aln_file}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python fasta_to_aln.py <input_fasta_file> <output_aln_file>")
        sys.exit(1)
    
    input_fasta = sys.argv[1]
    output_aln = sys.argv[2]
    fasta_to_aln(input_fasta, output_aln)
