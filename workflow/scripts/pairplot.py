import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1) Läs in den fulla sekvens-listan
all_names = pd.read_csv("results/combined_results_with_pdb_paths.csv")["name"]

# 2) Slå på metrics (vänster-merge mot all_names)
metrics = pd.read_csv("results/combined_results_with_pdb_paths.csv")  # redan mergad enligt föregående skript

# 3) Ta fram bara de kolumner du vill plotta + Type
plot_df = metrics[[
    "STABILITY", "percent_disorder", "num_disorder_segments",
    "Hydrophobicity", "Sequence_Length", "Molecular_Weight",
    "pI", "TM_SCORE", "Type"
]]

# 4) Skapa pairplot utan att ta bort rader med NaN i *alla* kolumner:
g = sns.pairplot(plot_df, hue="Type", diag_kind="hist", dropna=False)
g.fig.suptitle("Rubisco Generated vs. Natural", y=1.02)

plt.tight_layout()
g.savefig("pairplot_results.png")
plt.show()
