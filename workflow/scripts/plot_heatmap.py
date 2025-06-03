import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap(input_file, output_file):
    df = pd.read_csv(input_file, sep="\t", index_col=0)
    df = df.apply(pd.to_numeric, errors='coerce')

    print("Matrix shape:", df.shape)
    print("NaN values:", df.isna().sum().sum())
    print("Min value:", df.min().min(), "Max value:", df.max().max())

    if df.isna().sum().sum() > 0:
        print("Error: matrix contains NaN values.")
        return

    plt.figure(figsize=(12, 10))
    sns.heatmap(
        df,
        cmap="viridis",
        linewidths=0.5,
        square=True,
        cbar_kws={'label': 'Distance'},
        vmin=0.1,       # sätt minimum för färgskala (justera efter data)
        vmax=0.8,       # sätt maximum för färgskala
        xticklabels=False,
        yticklabels=False
    )
    plt.title("Sequence Distance Heatmap")
    plt.tight_layout()
    plt.savefig(output_file, dpi=300)
    print(f"Heatmap saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python plot_heatmap.py <input_tsv> <output_png>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    plot_heatmap(input_file, output_file)
