import sys
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def plot_heatmap(input_file, output_file):
    df = pd.read_csv(input_file, sep="\t", index_col=0)

    plt.figure(figsize=(12, 10))
    sns.heatmap(df, cmap="viridis", linewidths=0.5, square=True, cbar_kws={'label': 'Distance'})
    plt.title("Sequence Distance Heatmap")
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"✅ Heatmap saved to: {output_file}")

if __name__ == "__main__":
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    plot_heatmap(input_file, output_file)
