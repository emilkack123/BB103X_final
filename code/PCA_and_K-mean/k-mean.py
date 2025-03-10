import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA  # Import PCA for dimensionality reduction
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

# Ensure padded_sequences is a numpy array
padded_sequences = np.array(padded_sequences)

# Standardize the data (optional but recommended)
scaler = StandardScaler()
scaled_sequences = scaler.fit_transform(padded_sequences)

# Perform K-means clustering with 2 clusters (changed from 3 to 2)
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(scaled_sequences)

# Get K-means cluster labels
labels = kmeans.labels_

# Apply PCA to reduce dimensionality to 2 for visualization
pca = PCA(n_components=2)
pca_result = pca.fit_transform(scaled_sequences)

# Define colors for the clusters manually
# Light red for Cluster 1 and Blue for Cluster 2
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

# Save the plot to a file
output_file = "/home/moa/BB103X_final/results/kmeans_plot_pca_with_clusters.png"
plt.savefig(output_file, dpi=300)

# Optional: Print confirmation message
print(f"K-means clustering plot saved to {output_file}")

# Close the plot
plt.close()
