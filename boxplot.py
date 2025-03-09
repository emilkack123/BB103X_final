import pandas as pd
import matplotlib.pyplot as plt

# Läs in CSV-filen. Antag att filen har en header.
df = pd.read_csv('results/pI_results.csv')

# Om filen har en kolumn med rubriken 'pI' används den, annars antas att pI-värdena finns i den andra kolumnen.
if 'pI' in df.columns:
    pI_values = df['pI']
else:
    # Om det finns mer än en kolumn, använd den andra (index 1). Annars använd första kolumnen.
    pI_values = df.iloc[:, 1] if df.shape[1] > 1 else df.iloc[:, 0]

# Notera: Om CSV-filen har en header så motsvarar rad 2–11 data med index 1–10,
# och rad 12–21 data med index 11–20.
group_genererade = pI_values.iloc[1:11]
group_naturliga = pI_values.iloc[11:21]

# Sätt ihop grupperna i en lista och definiera etiketter
data = [group_genererade, group_naturliga]
labels = ['Genererade', 'Naturliga']

# Rita boxplot
plt.figure(figsize=(8, 6))
plt.boxplot(data, labels=labels)
plt.ylabel('pI-värde')
plt.title('Boxplot av pI-resultat')
plt.savefig("boxplot.png")

