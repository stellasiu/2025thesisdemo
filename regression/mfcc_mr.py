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
# MULTIVARIATE REGRESSION: One model per phoneme using all formants
multi_results = []

for phoneme in unique_phonemes:
    train_subset = train_df[train_df['phoneme'] == phoneme]
    test_subset = test_df[test_df['phoneme'] == phoneme]

    if len(train_subset) < 10 or len(test_subset) < 5:
        continue

    X_train = train_subset[mfcc_features]
    y_train = train_subset['height_cm']
    X_test = test_subset[mfcc_features]
    y_test = test_subset['height_cm']

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    result = {
        'phoneme': phoneme,
        'rmse': rmse}
    multi_results.append(result)

# Create DataFrame
multi_df = pd.DataFrame(multi_results).set_index('phoneme')

# Save to .csv file for stat analysis
multi_df = pd.DataFrame(multi_results)
multi_df.to_csv("mfcc_mr_regression_results.csv", index=False)


# -------------------
# Plot 1: Heatmap of RMSE per Phoneme
plt.figure(figsize=(8, 6))
sns.heatmap(multi_df[['rmse']].sort_values('rmse'), annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'RMSE (cm)'})
plt.title("RMSE per Phoneme (Multivariate Regression)")
plt.xlabel("Metric")
plt.ylabel("Phoneme")
plt.tight_layout()
plt.show()

