import argparse
from Bio import SeqIO
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import matplotlib.lines as mlines

# Function to convert amino acid sequences to numerical form
def aa_to_numeric(seq):
    # Define a simple index for amino acids, for example: A=0, C=1, ..., Y=19
    aa_dict = {aa: idx for idx, aa in enumerate('ACDEFGHIKLMNPQRSTVWXY')}
    numeric_seq = [aa_dict.get(aa, 0) for aa in seq]  # Use 0 for unknown characters
    return numeric_seq

# Read the sequences from the FASTA file
def read_fasta(file_path):
    sequences = []
    print(f"Reading sequences from {file_path}...")  # Debugging line
    for record in SeqIO.parse(file_path, "fasta"):
        sequences.append(str(record.seq))
    print(f"Read {len(sequences)} sequences from {file_path}")  # Debugging line
    return sequences

def main(args):
    # Load your sequences from provided file paths
    print(f"Loading sequences from {args.input_fasta_1} and {args.input_fasta_2}...")  # Debugging line
    sequences_gen = read_fasta(args.input_fasta_1)  # Generated sequences
    sequences_nat = read_fasta(args.input_fasta_2)  # Natural sequences
    sequences = sequences_gen + sequences_nat  # Combine both sets
    print(f"Total sequences loaded: {len(sequences)}")  # Debugging line

    # Convert sequences to numerical form
    print("Converting sequences to numerical form...")  # Debugging line
    sequence_vectors = [aa_to_numeric(seq) for seq in sequences]
    print(f"First sequence (numerical): {sequence_vectors[0]}")  # Debugging line

    max_length = max(len(seq) for seq in sequence_vectors)  # Find the maximum length of all sequences
    print(f"Max sequence length: {max_length}")  # Debugging line

    # Pad shorter sequences with zeros
    print("Padding sequences to the maximum length...")  # Debugging line
    padded_sequences = [seq + [0] * (max_length - len(seq)) if len(seq) < max_length else seq for seq in sequence_vectors]

    # Standardize the data (optional but recommended)
    print("Standardizing the sequences...")  # Debugging line
    scaler = StandardScaler()
    scaled_sequences = scaler.fit_transform(padded_sequences)

    # Perform PCA to reduce dimensionality
    print("Performing PCA...")  # Debugging line
    pca = PCA(n_components=2)  # You can change the number of components if needed
    pca_result = pca.fit_transform(scaled_sequences)
    print(f"PCA explained variance ratio: {pca.explained_variance_ratio_}")  # Debugging line

    # Define labels for coloring (0 for generated sequences, 1 for natural sequences)
    labels = ['gen'] * len(sequences_gen) + ['nat'] * len(sequences_nat)

    # Create a color map for the labels
    colors = ['red' if label == 'gen' else 'blue' for label in labels]

    # Create the plot
    print("Creating the PCA plot...")  # Debugging line
    plt.figure(figsize=(8, 6))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=colors, marker='o', s=50, edgecolors='k', alpha=0.7)

    # Add title and labels
    plt.title("PCA of Amino Acid Sequences", fontsize=16, fontweight='bold')
    plt.xlabel("Principal Component 1", fontsize=14)
    plt.ylabel("Principal Component 2", fontsize=14)

    # Add gridlines
    plt.grid(True, linestyle='--', alpha=0.5)

    # Add legend
    gen_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='red', markersize=10, label='Generated Sequences')
    nat_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Natural Sequences')
    plt.legend(handles=[gen_legend, nat_legend], loc='best')

    # Save the plot to a file (provided by the user)
    print(f"Saving the plot to {args.output_plot}...")  # Debugging line
    plt.savefig(args.output_plot, dpi=300)

    # Optional: Print confirmation message
    print(f"PCA plot saved to {args.output_plot}")

    # Close the plot
    plt.close()

if __name__ == "__main__":
    # Set up argparse to get input and output file paths
    parser = argparse.ArgumentParser(description="PCA analysis of amino acid sequences")
    parser.add_argument("input_fasta_1", type=str, help="Path to the first FASTA file (generated sequences)")
    parser.add_argument("input_fasta_2", type=str, help="Path to the second FASTA file (natural sequences)")
    parser.add_argument("output_plot", type=str, help="Path to save the PCA plot")

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function with the parsed arguments
    main(args)
