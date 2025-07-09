import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# -------------------
# Load data
train_df = pd.read_csv("mfcc_train_phoneme_height.csv")
test_df = pd.read_csv("mfcc_test_phoneme_height.csv")

mfcc_features = [f'mfcc{i}' for i in range(1, 14)]
unique_phonemes = train_df['phoneme'].unique()

# -------------------
# SIMPLE REGRESSION: One formant at a time per phoneme
simple_results = []

for phoneme in unique_phonemes:
    for mfcc in mfcc_features:
        train_subset = train_df[train_df['phoneme'] == phoneme]
        test_subset = test_df[test_df['phoneme'] == phoneme]

        if len(train_subset) < 10 or len(test_subset) < 5:
            continue

        X_train = train_subset[[mfcc]]
        y_train = train_subset['height_cm']
        X_test = test_subset[[mfcc]]
        y_test = test_subset['height_cm']

        model = LinearRegression()
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

        simple_results.append({
            'phoneme': phoneme,
            'mfcc': mfcc,
            'rmse': rmse
        })

# -------------------
# Convert to DataFrame
simple_df = pd.DataFrame(simple_results)

# -------------------
# Display the results table
print("Simple Regression Results per Phoneme (MFCC):")
print(simple_df.sort_values(by='rmse'))

# -------------------
# Plot 1: Heatmap of RMSE per (Phoneme, Formant)
pivot_rmse = simple_df.pivot(index='phoneme', columns='mfcc', values='rmse')
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_rmse, annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'RMSE (cm)'})
plt.title("Simple Regression RMSE per (Phoneme, MFCC)")
plt.xlabel("MFCC")
plt.ylabel("Phoneme")
plt.tight_layout()
plt.show()

# -------- Compute mean RMSE per phoneme and save --------
results_df = pd.DataFrame(simple_results)  # Ensure simple_results has keys: 'phoneme' and 'rmse'
mean_rmse_per_phoneme = results_df.groupby("phoneme")["rmse"].mean().reset_index()
mean_rmse_per_phoneme.to_csv("mfcc_sr_regression_results.csv", index=False)
