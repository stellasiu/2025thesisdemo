import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# -------------------
# Load data
train_df = pd.read_csv("f0_train_phoneme_height.csv")
test_df = pd.read_csv("f0_test_phoneme_height.csv")

unique_phonemes = train_df['phoneme'].unique()

# -------------------
# SIMPLE REGRESSION using only f0 per phoneme
f0_results = []

for phoneme in unique_phonemes:
    train_subset = train_df[train_df['phoneme'] == phoneme]
    test_subset = test_df[test_df['phoneme'] == phoneme]

    if len(train_subset) < 10 or len(test_subset) < 5:
        continue

    X_train = train_subset[['f0']]
    y_train = train_subset['height_cm']
    X_test = test_subset[['f0']]
    y_test = test_subset['height_cm']

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    f0_results.append({
        'phoneme': phoneme,
        'rmse': rmse})


# -------------------
# Convert to DataFrame
f0_df = pd.DataFrame(f0_results).set_index('phoneme')

# -------------------
# Save to .csv file for stat
results_df = pd.DataFrame(f0_results)
results_df.to_csv("f0_regression_results.csv", index=False)

# -------------------
# Plot 1: Heatmap of RMSE per Phoneme
plt.figure(figsize=(8, 6))
sns.heatmap(f0_df[['rmse']].sort_values('rmse'), annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'RMSE (cm)'})
plt.title("Simple Regression RMSE per Phoneme (f0)")
plt.xlabel("Metric")
plt.ylabel("Phoneme")
plt.tight_layout()
plt.show()
