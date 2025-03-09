import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file. Assume that the file has a header.
df = pd.read_csv('results/pI_results.csv')

# If the file has a column with the header 'pI', use it; otherwise, assume that the pI values are in the second column.
if 'pI' in df.columns:
    pI_values = df['pI']
else:
    # If there is more than one column, use the second (index 1). Otherwise, use the first column.
    pI_values = df.iloc[:, 1] if df.shape[1] > 1 else df.iloc[:, 0]

# Note: If the CSV file has a header, then rows 2–11 correspond to data with indices 1–10,
# and rows 12–21 correspond to data with indices 11–20.
group_generated = pI_values.iloc[1:11]
group_natural = pI_values.iloc[11:21]

# Combine the groups into a list and define labels.
data = [group_generated, group_natural]
labels = ['Generated', 'Natural']

# Plot the boxplot.
plt.figure(figsize=(8, 6))
plt.boxplot(data, labels=labels)
plt.ylabel('pI-value')
plt.title('Boxplot of pI-results')
plt.savefig("boxplot.png")
