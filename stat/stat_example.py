import pandas as pd
from scipy.stats import friedmanchisquare
import seaborn as sns
import matplotlib.pyplot as plt

# Load the CSV files
f0_df = pd.read_csv("f0_regression_results.csv")
formants_df = pd.read_csv("formants_sr_regression_results.csv")
mfcc_df = pd.read_csv("mfcc_sr_regression_results.csv")

# Merge datasets on 'phoneme' column
merged_df = f0_df.merge(formants_df, on='phoneme', suffixes=('_f0', '_formants'))
merged_df = merged_df.merge(mfcc_df, on='phoneme')
merged_df.rename(columns={'rmse': 'rmse_mfcc'}, inplace=True)

# Perform Friedman test
statistic, p_value = friedmanchisquare(
    merged_df['rmse_f0'],
    merged_df['rmse_formants'],
    merged_df['rmse_mfcc']
)

# Print results
print("Friedman test statistic:", statistic)
print("P-value:", format(p_value, ".7f"))
if p_value < 0.05:
    print("Result is statistically significant (p < 0.05).")
else:
    print("Result is not statistically significant (p ≥ 0.05).")

# Prepare data for plotting
plot_df = pd.melt(merged_df, id_vars='phoneme',
                  value_vars=['rmse_f0', 'rmse_formants', 'rmse_mfcc'],
                  var_name='Feature_Set', value_name='RMSE')

# Beautify feature set names
plot_df['Feature_Set'] = plot_df['Feature_Set'].map({
    'rmse_f0': 'F0',
    'rmse_formants': 'Formants',
    'rmse_mfcc': 'MFCC'
})

# Plot
plt.figure(figsize=(8, 6))
sns.boxplot(x='Feature_Set', y='RMSE', data=plot_df)
sns.stripplot(x='Feature_Set', y='RMSE', data=plot_df, color='black', alpha=0.5, jitter=True)
plt.title("RMSE Comparison Across Feature Sets (SR)")
plt.ylabel("RMSE")
plt.xlabel("Feature Set")
plt.tight_layout()
plt.show()
