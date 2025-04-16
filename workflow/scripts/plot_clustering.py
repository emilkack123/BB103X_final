#!/usr/bin/env python3

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

def load_distance_matrix(file_path):
    dist_mat = pd.read_csv(file_path, index_col=0, header=None, skiprows=1, sep=r'\s+')
    dist_mat.index.name = None
    dist_mat.columns = dist_mat.index
    return dist_mat

def load_metadata(file_path):
    return pd.read_csv(file_path)

def plot_tsne(distance_matrix, output_file='tsne_plot.png', metadata=None,
              perplexity=None, force_pca=False):
    
    num_samples = distance_matrix.shape[0]

    # Auto or manual perplexity
    if perplexity is None:
        perplexity = min(30, max(2, num_samples // 3))  # Automatically tuned
    else:
        perplexity = max(2, min(perplexity, num_samples - 1))  # Clamp to valid range

    # Decide whether to apply PCA
    use_pca = force_pca or (num_samples <= 50)

    print(f"[INFO] Samples: {num_samples}")
    print(f"[INFO] Perplexity: {perplexity}")
    print(f"[INFO] Using PCA: {use_pca}")

    # Preprocess with PCA if needed
    if use_pca:
        pca = PCA(n_components=min(10, num_samples))
        tsne_input = pca.fit_transform(distance_matrix)
        tsne_metric = 'euclidean'
    else:
        tsne_input = distance_matrix
        tsne_metric = 'precomputed'

    tsne = TSNE(metric=tsne_metric,
                init='random',
                random_state=0,
                perplexity=perplexity)
    
    tsne_results = tsne.fit_transform(tsne_input)
    
    tsne_df = pd.DataFrame(tsne_results, columns=['t-SNE 1', 't-SNE 2'])
    tsne_df['id'] = distance_matrix.index

    plt.figure(figsize=(10, 8))
    
    if metadata is not None:
        tsne_df = tsne_df.merge(metadata, on='id', how='left')
        sns.scatterplot(data=tsne_df, x='t-SNE 1', y='t-SNE 2', hue='origin', palette='viridis')
    else:
        sns.scatterplot(data=tsne_df, x='t-SNE 1', y='t-SNE 2')
    
    plt.title("t-SNE Clustering of Sequences")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

    print(f"[INFO] t-SNE plot saved to: {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot t-SNE clustering from a distance matrix.')
    parser.add_argument('distance_matrix', type=str, help='Path to the distance matrix file (TSV format).')
    parser.add_argument('output_plot', type=str, help='Output file for the plot (e.g., tsne.png).')
    parser.add_argument('--metadata', type=str, help='Optional CSV file with columns: id, origin')
    parser.add_argument('--perplexity', type=int, default=None, help='Optional perplexity override (e.g., 5)')
    parser.add_argument('--force_pca', action='store_true', help='Force PCA preprocessing regardless of sample size')

    args = parser.parse_args()

    distance_matrix = load_distance_matrix(args.distance_matrix)
    metadata = load_metadata(args.metadata) if args.metadata else None

    plot_tsne(
        distance_matrix=distance_matrix,
        output_file=args.output_plot,
        metadata=metadata,
        perplexity=args.perplexity,
        force_pca=args.force_pca
    )
