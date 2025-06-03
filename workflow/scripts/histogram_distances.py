import pandas as pd
import matplotlib.pyplot as plt

# 1. Load the distance matrix (tab‐separated, row & column labels in the first column)
df = pd.read_csv("results/distmat.tsv", sep="\t", index_col=0)

# 2. Convert to numeric (just in case there were stray strings)
df = df.apply(pd.to_numeric, errors="coerce")

# 3. Extract only the off-diagonal entries
#    (we don’t want the zeros on the diagonal).
#
#    One easy way: stack the DataFrame, then filter out where row == column.
distances = (
    df.stack()              # turns into a Series whose index is (row_id, col_id)
      .reset_index()        # make “row_id” and “col_id” real columns
      .rename(columns={0: "Distance", "level_0": "Row", "level_1": "Col"})
)
offdiag = distances[distances["Row"] != distances["Col"]]["Distance"]

# 4. Plot histogram of those off‐diagonal distances
plt.figure(figsize=(6, 4))
plt.hist(offdiag, bins=50, color="steelblue", edgecolor="black")
plt.xlabel("Pairwise Distance")
plt.ylabel("Frequency")
plt.title("Histogram of All Pairwise Distances (off-diagonal)")
plt.tight_layout()
plt.savefig("results/distance_histogram.png", dpi=200)
plt.show()
