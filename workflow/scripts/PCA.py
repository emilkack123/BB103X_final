import argparse
from Bio import SeqIO
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import matplotlib.lines as mlines

# Function to convert amino acid sequences to numerical form
def aa_to_numeric(seq):
    aa_dict = {aa: idx for idx, aa in enumerate('ACDEFGHIKLMNPQRSTVWXY')}
    return [aa_dict.get(aa, 0) for aa in seq]  # Use 0 for unknown characters

# Read the sequences from the FASTA file
def read_fasta(file_path):
    sequences = []
    print(f"Reading sequences from {file_path}...")
    for record in SeqIO.parse(file_path, "fasta"):
        sequences.append(str(record.seq))
    print(f"Read {len(sequences)} sequences from {file_path}")
    return sequences

def main(args):
    # Load sequences
    print(f"Loading sequences from {args.input_fasta_1} and {args.input_fasta_2}...")
    sequences_gen = read_fasta(args.input_fasta_1)
    sequences_nat = read_fasta(args.input_fasta_2)
    sequences = sequences_gen + sequences_nat
    print(f"Total sequences loaded: {len(sequences)}")

    # Convert sequences to numerical form
    print("Converting sequences to numerical form...")
    sequence_vectors = [aa_to_numeric(seq) for seq in sequences]
    max_length = max(len(seq) for seq in sequence_vectors)
    print(f"Max sequence length: {max_length}")

    # Pad shorter sequences with zeros
    padded_sequences = [seq + [0] * (max_length - len(seq)) for seq in sequence_vectors]

    # Standardize the data
    print("Standardizing the sequences...")
    scaler = StandardScaler()
    scaled_sequences = scaler.fit_transform(padded_sequences)

    # Perform PCA (with enough components for scree plot)
    print("Performing PCA...")
    pca = PCA(n_components=min(len(scaled_sequences), len(scaled_sequences[0])))  # All possible components
    pca_result = pca.fit_transform(scaled_sequences)
    print(f"PCA explained variance ratio: {pca.explained_variance_ratio_}")

    # Define labels and colors for PCA plot
    labels = ['gen'] * len(sequences_gen) + ['nat'] * len(sequences_nat)
    colors = ['red' if label == 'gen' else 'blue' for label in labels]

    # Create the PCA plot
    print("Creating the PCA plot...")
    plt.figure(figsize=(8, 6))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=colors, marker='o', s=50, edgecolors='k', alpha=0.7)
    plt.title("PCA of Amino Acid Sequences", fontsize=16, fontweight='bold')
    plt.xlabel("Principal Component 1", fontsize=14)
    plt.ylabel("Principal Component 2", fontsize=14)
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(handles=[
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor='red', markersize=10, label='Generated Sequences'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Natural Sequences')
    ], loc='best')
    print(f"Saving PCA plot to {args.output_plot}...")
    plt.savefig(args.output_plot, dpi=300)
    plt.close()

    # Create the Scree Plot
    print("Creating the scree plot...")
    plt.figure(figsize=(8, 6))
    plt.plot(range(1, len(pca.explained_variance_ratio_) + 1), pca.explained_variance_ratio_, marker='o', linestyle='-', color='b')
    plt.xlabel("Principal Component", fontsize=14)
    plt.ylabel("Explained Variance Ratio", fontsize=14)
    plt.title("Scree Plot", fontsize=16, fontweight='bold')
    plt.grid(True, linestyle='--', alpha=0.5)

    # Save the scree plot
    scree_plot_path = args.output_plot.replace(".png", "_scree.png")
    print(f"Saving the scree plot to {scree_plot_path}...")
    plt.savefig(scree_plot_path, dpi=300)
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCA analysis of amino acid sequences")
    parser.add_argument("input_fasta_1", type=str, help="Path to the first FASTA file (generated sequences)")
    parser.add_argument("input_fasta_2", type=str, help="Path to the second FASTA file (natural sequences)")
    parser.add_argument("output_plot", type=str, help="Path to save the PCA plot")
    args = parser.parse_args()
    main(args)
