import sys
import pandas as pd
from Bio import SeqIO
from Bio import pairwise2

def sequence_identity(seq1, seq2):
    alignments = pairwise2.align.globalxx(seq1, seq2, one_alignment_only=True)
    aligned_seq1, aligned_seq2 = alignments[0][:2]
    matches = sum(a == b for a, b in zip(aligned_seq1, aligned_seq2))
    return matches / max(len(seq1), len(seq2))

def compute_distance_matrix(fasta1, fasta2, output_file):
    records1 = list(SeqIO.parse(fasta1, "fasta"))
    records2 = list(SeqIO.parse(fasta2, "fasta"))
    all_records = records1 + records2

    ids = [record.id for record in all_records]
    n = len(all_records)

    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == j:
                row.append(0.0)
            elif i > j:
                row.append(matrix[j][i])
            else:
                seq1 = str(all_records[i].seq)
                seq2 = str(all_records[j].seq)
                distance = 1 - sequence_identity(seq1, seq2)
                row.append(round(distance, 4))
        matrix.append(row)

    df = pd.DataFrame(matrix, index=ids, columns=ids)
    df.to_csv(output_file, sep="\t")

if __name__ == "__main__":
    fasta1 = sys.argv[1]
    fasta2 = sys.argv[2]
    output_file = sys.argv[3]
    compute_distance_matrix(fasta1, fasta2, output_file)
