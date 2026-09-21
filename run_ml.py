"""Phase 4 ML: Traffic speed prediction experiment.

Uses the extracted dataset: data/processed/ecoroute_ml_dataset.csv
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

# Load data
df = pd.read_csv('data/processed/ecoroute_ml_dataset.csv')

# Sort by time chronologically
df = df.sort_values('time').reset_index(drop=True)

# Chronological 80/20 split
train_size = int(0.8 * len(df))
train_df = df.iloc[:train_size]
test_df = df.iloc[train_size:]

features = ['hour', 'day_of_week', 'month', 'length', 'bus_count', 'message_count', 'segment_id']

y = df['speed']

# ============================================================
# 1. Linear Regression
# ============================================================
lin_reg = LinearRegression()
lin_reg.fit(train_df[features], train_df['speed'])
y_train_pred_lin = lin_reg.predict(train_df[features])
y_test_pred_lin = lin_reg.predict(test_df[features])

def evaluate(y_true, y_pred):
    mae = np.mean(np.abs(y_true - y_pred))
    mse = np.mean((y_true - y_pred)**2)
    rmse = np.sqrt(mse)
    from sklearn.metrics import r2_score
    r2 = r2_score(y_true, y_pred)
    return {'MAE': mae, 'RMSE': rmse, 'R2': r2}

# 2. Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(train_df[features], train_df['speed'])
y_train_pred_rf = rf.predict(train_df[features])
y_test_pred_rf = rf.predict(test_df[features])

# 3. Gradient Boosting
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(train_df[features], train_df['speed'])
y_train_pred_gb = gb.predict(train_df[features])
y_test_pred_gb = gb.predict(test_df[features])

# Print results
print('='*60)
print('EXPERIMENTAL TRAFFIC SPEED PREDICTION')
print('='*60)
print(f'Dataset: 620 observations from June 2024 (7 days, limited hours)')
print(f'Chronological 80/20 train/test split')
print()

# Helper
def m(y_true, y_pred):
    return evaluate(y_true, y_pred)

print('--- Linear Regression ---')
train_metrics_lin = evaluate(y_train, y_train_pred_lin)
test_metrics_lin = evaluate(y_test, y_test_pred_lin)
print(f'Train: MAE={train_metrics_lin["MAE"]:.2f}, RMSE={train_metrics_lin["RMSE"]:.2f}, R2={train_metrics_lin["R2"]:.3f}')
print(f'Test:  MAE={test_metrics_lin["MAE"]:.2f}, RMSE={test_metrics_lin["RMSE"]:.2f}, R2={test_metrics_lin["R2"]:.3f}')

print('\\n--- Random Forest ---')
train_metrics_rf = evaluate(y_train, y_train_pred_rf)
test_metrics_rf = evaluate(y_test, y_test_pred_rf)
print(f'Train: MAE={train_metrics_rf["MAE"]:.2f}, RMSE={train_metrics_rf["RMSE"]:.2f}, R2={train_metrics_rf["R2"]:.3f}')
print(f'Test:  MAE={test_metrics_rf["MAE"]:.2f}, RMSE={test_metrics_rf["RMSE"]:.2f}, R2={test_metrics_rf["R2"]:.3f}')

print('\\n--- Gradient Boosting ---')
train_metrics_gb = evaluate(y_train, y_train_pred_gb)
test_metrics_gb = evaluate(y_test, y_test_pred_gb)
print(f'Train: MAE={train_metrics_gb["MAE"]:.2f}, RMSE={train_metrics_gb["RMSE"]:.2f}, R2={train_metrics_gb["R2"]:.3f}')
print(f'Test:  MAE={test_metrics_gb["MAE"]:.2f}, RMSE={test_metrics_gb["RMSE"]:.2f}, R2={test_metrics_gb["R2"]:.3f}')

# ============================================================
# Plot 1: Actual vs. Predicted (Test set)
# ============================================================
import matplotlib.pyplot as plt
import seaborn as sns

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.scatterplot(x=y_test, y=y_test_pred_lin, ax=axes[0], alpha=0.3)
axes[0].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[0].set_xlabel('Actual Speed (mph)')
axes[0].set_ylabel('Predicted Speed (mph)')
axes[0].set_title('Linear Regression: Actual vs. Predicted')

sns.scatterplot(x=y_test, y=y_test_pred_rf, ax=axes[1], alpha=0.3)
axes[1].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
axes[1].set_xlabel('Actual Speed (mph)')
axes[1].set_ylabel('Predicted Speed (mph)')
axes[1].set_title('Random Forest: Actual vs. Predicted')

sns.scatterplot(x=y_test, y=y_test_pred_gb, ax=axes[2], alpha=0.3)
axes[2].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'g--', lw=2)
axes[2].set_xlabel('Actual Speed (mph)')
axes[2].set_ylabel('Predicted Speed (mph)')
axes[2].set_title('Gradient Boosting: Actual vs. Predicted')

plt.tight_layout()
plt.savefig('reports/figures/actual_vs_predicted.png', dpi=150)
plt.show()

# ============================================================
# Plot 2: Residuals (Linear Regression)
# ============================================================
residuals_lin = y_test - y_test_pred_lin
plt.figure(figsize=(8, 4))
sns.histplot(residuals_lin, bins=30, kde=True)
plt.title('Linear Regression: Residual Distribution')
plt.xlabel('Residual (Actual - Predicted, mph)')
plt.ylabel('Frequency')
plt.tight_layout()
plt.savefig('reports/figures/residuals_lin.png', dpi=150)
plt.show()

# ============================================================
# Plot 3: Feature importance (Random Forest)
# ============================================================
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(8, 4))
plt.title('Random Forest: Feature Importance')
plt.bar(range(len(features)), importances[indices], align='middle')
plt.xticks(range(len(features)), [str(features[i]) for i in indices])
plt.xlabel('Feature')
plt.ylabel('Importance')
plt.tight_layout()
plt.savefig('reports/figures/feature_importance_rf.png', dpi=150)
plt.show()

# ============================================================
# Save model
# ============================================================
joblib.dump(rf, 'models/traffic_speed_model.pkl')
print('Model saved as models/traffic_speed_model.pkl')

# ============================================================
# Results summary
# ============================================================
print('\\n' + '='*60)
print('EXPERIMENTAL RESULTS SUMMARY')
print('='*60)
print('Dataset: 620 observations from June 2024 (7 days, limited hours)')
print('Target: speed (mph)')
print('Features:', features)
print('Train/test: 80/20 chronological split')
print()
print('Linear Regression (Test): MAE={:.2f}, RMSE={:.2f}, R2={:.3f}'.format(test_metrics_lin["MAE"], test_metrics_lin["RMSE"], test_metrics_lin["R2"]))
print('Random Forest (Test): MAE={:.2f}, RMSE={:.2f}, R2={:.3f}'.format(test_metrics_rf["MAE"], test_metrics_rf["RMSE"], test_metrics_rf["R2"]))
print('Gradient Boosting (Test): MAE={:.2f}, RMSE={:.2f}, R2={:.3f}'.format(test_metrics_gb["MAE"], test_metrics_gb["RMSE"], test_metrics_gb["R2"]))
print()
print('IMPORTANT: These are prototype results on a limited API-derived sample.')
print('Do NOT present as guaranteed real-world traffic speeds.')
print('Dataset covers only June 2024, limited hours, limited segments.')
print()
print('Model and results saved. Next: generate traffic_model_results.csv and docs/ml_results.md')
"