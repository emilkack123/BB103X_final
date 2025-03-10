import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file. Adjust the file path as needed.
df = pd.read_csv('results/hydrophobicity_results.csv')

# If the file has a column 'hydrophobicity', use it; otherwise, assume the hydrophobicity values are in the second column.
if 'hydrophobicity' in df.columns:
    hydro_values = df['hydrophobicity']
else:
    hydro_values = df.iloc[:, 1] if df.shape[1] > 1 else df.iloc[:, 0]

# Convert hydrophobicity values to numeric, coercing errors to NaN.
hydro_values = pd.to_numeric(hydro_values, errors='coerce')

# Optionally, drop NaN values if needed.
hydro_values = hydro_values.dropna()

# Note: If the CSV has a header, then rows 2–11 correspond to data with indices 1–10,
# and rows 12–21 correspond to data with indices 11–20.
group_generated = df['Hydrophobicity'].iloc[0:10]
group_natural   = df['Hydrophobicity'].iloc[10:20]

data = [group_generated, group_natural]
labels = ['Generated', 'Natural']

plt.boxplot(data, labels=labels)
plt.ylabel('Hydrophobicity')
plt.title('Boxplot of Hydrophobicity Results')
plt.savefig("hydrophobicity_boxplot.png")
plt.show()
