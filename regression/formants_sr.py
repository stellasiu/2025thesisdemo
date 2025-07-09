import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# -------------------
# Load data
train_df = pd.read_csv("formants_train_phoneme_height.csv")
test_df = pd.read_csv("formants_test_phoneme_height.csv")

formant_features = [f'f{i}' for i in range(1, 5)]
unique_phonemes = train_df['phoneme'].unique()

# -------------------
# SIMPLE REGRESSION: One formant at a time per phoneme
simple_results = []

for phoneme in unique_phonemes:
    for formant in formant_features:
        train_subset = train_df[train_df['phoneme'] == phoneme]
        test_subset = test_df[test_df['phoneme'] == phoneme]

        if len(train_subset) < 10 or len(test_subset) < 5:
            continue

        X_train = train_subset[[formant]]
        y_train = train_subset['height_cm']
        X_test = test_subset[[formant]]
        y_test = test_subset['height_cm']

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        simple_results.append({
            'phoneme': phoneme,
            'formant': formant,
            'rmse': rmse})

# -------------------
# Convert to DataFrame
simple_df = pd.DataFrame(simple_results)

# -------------------
# Plot 1: Heatmap of RMSE per (Phoneme, Formant)
pivot_rmse = simple_df.pivot(index='phoneme', columns='formant', values='rmse')
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_rmse, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'RMSE (cm)'})
plt.title("Simple Regression RMSE per (Phoneme, Formant)")
plt.xlabel("Formant")
plt.ylabel("Phoneme")
plt.tight_layout()
plt.show()

# -------- Compute mean RMSE per phoneme and save --------
results_df = pd.DataFrame(simple_results)  # Ensure simple_results has keys: 'phoneme' and 'rmse'
mean_rmse_per_phoneme = results_df.groupby("phoneme")["rmse"].mean().reset_index()
mean_rmse_per_phoneme.to_csv("formants_sr_regression_resuls.csv", index=False)
