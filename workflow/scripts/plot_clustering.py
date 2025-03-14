#!/usr/bin/env python3

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def load_distance_matrix(file_path):
    dist_mat = pd.read_csv(file_path, index_col=0, header=None, skiprows=1, sep=r'\s+')
    dist_mat.index.name = None
    dist_mat.columns = dist_mat.index
    return dist_mat

def load_metadata(file_path):
    return pd.read_csv(file_path)

def plot_tsne(distance_matrix, output_file='tsne_plot.png', metadata=None):
    tsne = TSNE(metric='precomputed', init='random', random_state=0)
    tsne_results = tsne.fit_transform(distance_matrix)
    
    tsne_df = pd.DataFrame(tsne_results, columns=['t-SNE 1', 't-SNE 2'])
    tsne_df['id'] = distance_matrix.index
    
    plt.figure(figsize=(10, 8))
    
    if metadata is not None:
        tsne_df = tsne_df.merge(metadata, on='id')
        sns.scatterplot(data=tsne_df, x='t-SNE 1', y='t-SNE 2', hue='origin', palette='viridis')
    else:
        sns.scatterplot(data=tsne_df, x='t-SNE 1', y='t-SNE 2')
    
    plt.savefig(output_file)
    plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot t-SNE clustering from a distance matrix.')
    parser.add_argument('distance_matrix', type=str, help='Path to the distance matrix file (TSV format).')
    parser.add_argument('output_plot', type=str, default='tsne_plot.png', help='Output file for the plot (default: tsne_plot.png).')
    parser.add_argument('--metadata', type=str, help='Optional CSV file containing IDs and origins for coloring the plot.')
    
    args = parser.parse_args()
    
    distance_matrix = load_distance_matrix(args.distance_matrix)
    metadata = load_metadata(args.metadata) if args.metadata else None
    plot_tsne(distance_matrix, args.output_plot, metadata)