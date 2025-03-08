import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from Bio import SeqIO
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
    for record in SeqIO.parse(file_path, "fasta"):
        sequences.append(str(record.seq))
    return sequences

# Load your sequences
file_path_1 = "/home/moa/BB103X_final/resources/gen.fa"
file_path_2 = "/home/moa/BB103X_final/resources/nat.fa"
sequences_gen = read_fasta(file_path_1)  # Generated sequences
sequences_nat = read_fasta(file_path_2)  # Natural sequences
sequences = sequences_gen + sequences_nat  # Combine both sets

# Convert sequences to numerical form
sequence_vectors = [aa_to_numeric(seq) for seq in sequences]

# Find the maximum length of all sequences
max_length = max(len(seq) for seq in sequence_vectors)

# Pad shorter sequences with zeros to make all sequences the same length
padded_sequences = [seq + [0] * (max_length - len(seq)) if len(seq) < max_length else seq for seq in sequence_vectors]

# Standardize the data (optional but recommended)
scaler = StandardScaler()
scaled_sequences = scaler.fit_transform(padded_sequences)

# Perform K-means clustering
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(scaled_sequences)

# Define labels for coloring (0 for generated sequences, 1 for natural sequences)
labels = ['gen'] * len(sequences_gen) + ['nat'] * len(sequences_nat)

# Create a color map for the labels
colors = ['red' if label == 'gen' else 'blue' for label in labels]

# Create the plot
plt.figure(figsize=(8, 6))
plt.scatter(scaled_sequences[:, 0], scaled_sequences[:, 1], c=colors, marker='o', s=50, edgecolors='k', alpha=0.7)

# Add title and labels
plt.title("K-means Clustering of Amino Acid Sequences", fontsize=16, fontweight='bold')
plt.xlabel("Feature 1", fontsize=14)
plt.ylabel("Feature 2", fontsize=14)

# Add gridlines
plt.grid(True, linestyle='--', alpha=0.5)

# Add legend
gen_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='red', markersize=10, label='Generated Sequences')
nat_legend = mlines.Line2D([], [], marker='o', color='w', markerfacecolor='blue', markersize=10, label='Natural Sequences')
plt.legend(handles=[gen_legend, nat_legend], loc='best')

# Save the plot to a file (e.g., 'kmeans_plot.png')
output_file = "/home/moa/BB103X_final/results/kmeans_plot.png"
plt.savefig(output_file, dpi=300)

# Optional: Print confirmation message
print(f"K-means clustering plot saved to {output_file}")

# Close the plot
plt.close()
