import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA  # Import PCA for dimensionality reduction
from Bio import SeqIO
import matplotlib.lines as mlines
import argparse
import os

# Function to convert amino acid sequences to numerical form
def aa_to_numeric(seq):
    # Define a simple index for amino acids, for example: A=0, C=1, ..., Y=19
    aa_dict = {aa: idx for idx, aa in enumerate('ACDEFGHIKLMNPQRSTVWXY')}
    numeric_seq = [aa_dict.get(aa, 0) for aa in seq]  # Use 0 for unknown characters
    return numeric_seq

# Read the sequences from the FASTA file
def read_fasta(file_path):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist.")
        exit(1)

    sequences = []
    for record in SeqIO.parse(file_path, "fasta"):
        sequences.append(str(record.seq))
    
    print(f"Loaded {len(sequences)} sequences from {file_path}.")
    return sequences

def main(args):
    # Load your sequences from provided file paths
    sequences_gen = read_fasta(args.input_fasta_1)  # Generated sequences
    sequences_nat = read_fasta(args.input_fasta_2)  # Natural sequences
    sequences = sequences_gen + sequences_nat  # Combine both sets

    # Check if there are any sequences to process
    if len(sequences) == 0:
        print("Error: No sequences loaded.")
        exit(1)

    # Convert sequences to numerical form
    sequence_vectors = [aa_to_numeric(seq) for seq in sequences]

    # Find the maximum length of all sequences
    max_length = max(len(seq) for seq in sequence_vectors)
    print(f"Maximum sequence length: {max_length}")

    # Pad shorter sequences with zeros to make all sequences the same length
    padded_sequences = [seq + [0] * (max_length - len(seq)) if len(seq) < max_length else seq for seq in sequence_vectors]

    # Ensure padded_sequences is a numpy array
    padded_sequences = np.array(padded_sequences)

    # Standardize the data (optional but recommended)
    scaler = StandardScaler()
    scaled_sequences = scaler.fit_transform(padded_sequences)

    # Perform K-means clustering with 2 clusters
    kmeans = KMeans(n_clusters=2, random_state=42)
    kmeans.fit(scaled_sequences)

    # Get K-means cluster labels
    labels = kmeans.labels_

    # Apply PCA to reduce dimensionality to 2 for visualization
    pca = PCA(n_components=2)
    pca_result = pca.fit_transform(scaled_sequences)

    # Define colors for the clusters manually
    colors = ['lightcoral' if label == 0 else 'blue' for label in labels]

    # Create the plot using PCA result and K-means labels
    plt.figure(figsize=(8, 6))
    plt.scatter(pca_result[:, 0], pca_result[:, 1], c=colors, marker='o', s=50, edgecolors='k', alpha=0.7)

    # Add title and labels
    plt.title("K-means Clustering of Amino Acid Sequences (PCA)", fontsize=16, fontweight='bold')
    plt.xlabel("PCA Feature 1", fontsize=14)
    plt.ylabel("PCA Feature 2", fontsize=14)

    # Add gridlines
    plt.grid(True, linestyle='--', alpha=0.5)

    # Add legend (optional)
    handles = [
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor='lightcoral', markersize=10, label='Cluster 1 (Light Red)'),
        mlines.Line2D([], [], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Cluster 2 (Blue)')
    ]
    plt.legend(handles=handles, loc='best')

    # Check if output directory exists
    output_dir = os.path.dirname(args.output_plot)
    if not os.path.exists(output_dir):
        print(f"Output directory {output_dir} does not exist. Creating it.")
        os.makedirs(output_dir)

    # Save the plot to a file
    try:
        plt.savefig(args.output_plot, dpi=300)
        print(f"K-means clustering plot saved to {args.output_plot}")
    except Exception as e:
        print(f"Error saving plot: {e}")
        exit(1)

    # Close the plot
    plt.close()

if __name__ == "__main__":
    # Set up argparse to get input and output file paths
    parser = argparse.ArgumentParser(description="K-means clustering of amino acid sequences with PCA visualization.")
    parser.add_argument("input_fasta_1", type=str, help="Path to the first FASTA file (generated sequences)")
    parser.add_argument("input_fasta_2", type=str, help="Path to the second FASTA file (natural sequences)")
    parser.add_argument("output_plot", type=str, help="Path to save the K-means clustering plot")

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function with the parsed arguments
    main(args)
