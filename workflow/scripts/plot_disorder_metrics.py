import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Generate disorder metric plots from IUPred results")
    parser.add_argument("input_csv", help="Path to disorder_metrics.csv")
    parser.add_argument("-o", "--output_dir", default="results/disorder_plots", help="Directory to save plots")
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)

    # Plot style
    sns.set(style="whitegrid", font_scale=1.2)
    os.makedirs(args.output_dir, exist_ok=True)

    # 1. Histogram: Percent Disorder
    plt.figure(figsize=(8, 5))
    sns.histplot(df["percent_disorder"], bins=30, kde=True, color="skyblue", edgecolor="black")
    plt.axvline(df["percent_disorder"].mean(), color='red', linestyle='--', label=f"Mean = {df['percent_disorder'].mean():.2f}")
    plt.title("Distribution of Percent Disorder")
    plt.xlabel("Percent Disorder")
    plt.ylabel("Number of Sequences")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/hist_percent_disorder.png")
    plt.close()

    # 2. Histogram: Disorder Segments
    plt.figure(figsize=(8, 5))
    sns.histplot(df["num_disorder_segments"], bins=30, kde=False, color="salmon", edgecolor="black")
    plt.axvline(df["num_disorder_segments"].mean(), color='red', linestyle='--', label=f"Mean = {df['num_disorder_segments'].mean():.1f}")
    plt.title("Distribution of Disorder Segment Counts")
    plt.xlabel("Number of Disorder Segments")
    plt.ylabel("Number of Sequences")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/hist_disorder_segments.png")
    plt.close()

    # 3. Scatter Plot
    plt.figure(figsize=(8, 6))
    sns.scatterplot(data=df, x="percent_disorder", y="num_disorder_segments", s=50, color="mediumseagreen")
    sns.regplot(data=df, x="percent_disorder", y="num_disorder_segments", scatter=False, color="black", line_kws={"linestyle": "--"})
    plt.title("Scatter Plot: Percent Disorder vs. Number of Segments")
    plt.xlabel("Percent Disorder")
    plt.ylabel("Number of Disorder Segments")
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/scatter_disorder_vs_segments.png")
    plt.close()

    # 4. Optional KDE Plot
    plt.figure(figsize=(8, 6))
    sns.kdeplot(data=df, x="percent_disorder", y="num_disorder_segments", cmap="viridis", fill=True, thresh=0.02, levels=100)
    plt.title("Density Plot: Percent Disorder vs. Disorder Segments")
    plt.xlabel("Percent Disorder")
    plt.ylabel("Number of Disorder Segments")
    plt.tight_layout()
    plt.savefig(f"{args.output_dir}/density_disorder.png")
    plt.close()

    print(f"✅ Plots saved to: {args.output_dir}")

if __name__ == "__main__":
    main()
