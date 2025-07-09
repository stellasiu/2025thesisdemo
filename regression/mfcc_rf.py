import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

# Load datasets
train_df = pd.read_csv("mfcc_train_phoneme_height.csv")
test_df = pd.read_csv("mfcc_test_phoneme_height.csv")

# MFCC feature list
mfcc_features = [f'mfcc{i}' for i in range(1, 14)]
unique_phonemes = train_df['phoneme'].unique()

# Store results
phoneme_results = []

# Per-phoneme model training and evaluation
for phoneme in unique_phonemes:
    X_train_p = train_df[train_df['phoneme'] == phoneme][mfcc_features]
    y_train_p = train_df[train_df['phoneme'] == phoneme]['height_cm']
    X_test_p = test_df[test_df['phoneme'] == phoneme][mfcc_features]
    y_test_p = test_df[test_df['phoneme'] == phoneme]['height_cm']

    if len(X_train_p) < 10 or len(X_test_p) < 5:
        continue  # skip small samples

    model = RandomForestRegressor(n_estimators=20, max_depth=10, random_state=42)
    model.fit(X_train_p, y_train_p)
    y_pred_p = model.predict(X_test_p)
    rmse_p = np.sqrt(mean_squared_error(y_test_p, y_pred_p))

    importances = model.feature_importances_
    phoneme_results.append({
        'phoneme': phoneme,
        'rmse': rmse_p,
        **{f: imp for f, imp in zip(mfcc_features, importances)}
    })

# Convert to DataFrame
phoneme_df = pd.DataFrame(phoneme_results).set_index('phoneme')



# -------------------
# Plot 1: MFCC Importance Heatmap
plt.figure(figsize=(14, 8))
sns.heatmap(phoneme_df.drop(columns='rmse'), annot=True, fmt=".2f", cmap="viridis", cbar_kws={'label': 'Feature Importance'})
plt.title("MFCC Feature Importance per Phoneme for Height Prediction")
plt.xlabel("MFCC Feature")
plt.ylabel("Phoneme")
plt.tight_layout()
plt.show()

# -------------------
# Plot 2: RMSE Heatmap
plt.figure(figsize=(8, 6))
sns.heatmap(phoneme_df[['rmse']].sort_values('rmse'), annot=True, fmt=".2f", cmap="coolwarm", cbar_kws={'label': 'RMSE (cm)'})
plt.title("Height Prediction RMSE per Phoneme")
plt.xlabel("Metric")
plt.ylabel("Phoneme")
plt.tight_layout()
plt.show()

# -------- Compute mean RMSE per phoneme and save --------
results_df = pd.DataFrame(phoneme_df)  # Ensure simple_results has keys: 'phoneme' and 'rmse'
mean_rmse_per_phoneme = results_df.groupby("phoneme")["rmse"].mean().reset_index()
mean_rmse_per_phoneme.to_csv("mfcc_rf_regression_results.csv", index=False)


