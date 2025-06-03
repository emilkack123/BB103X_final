# ─── Cell 1: Imports & Setup ─────────────────────────────────────────────────────────
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



# ─── Cell 2: Load the Distance Matrix ────────────────────────────────────────────────
# Make sure this path is correct relative to your notebook
distmat_path = "results/distmat.tsv"

# Read the TSV into a DataFrame, with the first column as row index
df = pd.read_csv(distmat_path, sep="\t", index_col=0).apply(pd.to_numeric, errors="coerce")

print("Matrix shape:", df.shape)
print("Any NaNs in matrix? →", df.isna().sum().sum())
print(df.describe().loc[['min','50%','max']])

# ─── Cell 3: Confirm Gallionella ID Exists ───────────────────────────────────────────
gall_id = "OGS68397.1"
if gall_id not in df.index:
    raise KeyError(f"'{gall_id}' not found in the distance‐matrix index!")
else:
    print(f"✅ '{gall_id}' found at row/column index {df.index.get_loc(gall_id)}.")

# ─── Cell 4: Extract & Sort Distances ───────────────────────────────────────────────
# Grab the entire row (distances from Gallionella to every sequence), drop itself
dist_series = df.loc[gall_id].drop(labels=[gall_id])

# Sort ascending (closest first)
neighbors_sorted = dist_series.sort_values()

# Optional: Convert to a DataFrame to tag “Type”
def seq_type(seq_id):
    return "Generated" if "_" in seq_id else "Natural"

neighbors_df = pd.DataFrame({
    "Neighbor": neighbors_sorted.index,
    "Distance": neighbors_sorted.values
})
neighbors_df["Type"] = neighbors_df["Neighbor"].apply(seq_type)

# ─── Cell 5: Show the Full Sorted List ───────────────────────────────────────────────
# This prints every sequence, sorted by distance to OGS68397.1.
# If you only want the top N, you can do neighbors_df.head(N).
neighbors_df

# ─── Cell 6 (Optional): Plot a Histogram of Distances from Gallionella ─────────────
plt.figure(figsize=(5, 4))
plt.hist(neighbors_df["Distance"], bins=50, color="steelblue", edgecolor="black")
plt.xlabel("Distance to OGS68397.1")
plt.ylabel("Frequency")
plt.title("Histogram of Gallionella’s Pairwise Distances")
plt.tight_layout()
plt.show()
