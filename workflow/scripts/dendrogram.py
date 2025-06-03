import sys
import pandas as pd
import numpy as np
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
from scipy.spatial.distance import squareform

def plot_dendrogram(input_file, output_file):
    # 1) Read in the distance matrix (TSV with sequence IDs as row and column headers)
    df = pd.read_csv(input_file, sep="\t", index_col=0)
    
    # 2) Ensure all values are numeric
    df = df.apply(pd.to_numeric, errors='coerce')
    
    # 3) Check for any NaN values
    total_nans = df.isna().sum().sum()
    if total_nans > 0:
        print(f"❌ Error: Distance matrix contains {total_nans} NaN values.")
        sys.exit(1)
    
    # 4) Convert the square distance matrix to a condensed 1D array for linkage
    #    (scipy's linkage expects a condensed distance array)
    dist_array = squareform(df.values)
    
    # 5) Perform hierarchical clustering (using average linkage here)
    Z = sch.linkage(dist_array, method="average")
    
    # 6) Plot the dendrogram
    plt.figure(figsize=(10, 8))
    sch.dendrogram(
        Z,
        labels=df.index.tolist(),
        orientation='right',    # Draw branches horizontally
        leaf_font_size=4,       # Very small font so many leaves can fit
        color_threshold=0.5     # Change this to adjust cluster-color cutoff
    )
    plt.title("Hierarchical Clustering Dendrogram")
    plt.xlabel("Distance")
    plt.ylabel("Sequence ID")
    plt.tight_layout()
    
    # 7) Save the figure
    plt.savefig(output_file, dpi=300)
    plt.close()
    print(f"✅ Dendrogram saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python dendrogram.py <input_tsv> <output_png>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    plot_dendrogram(input_file, output_file)
