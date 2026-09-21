"""Run ML experiment and create output files."""

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
df = df.sort_values('time').reset_index(drop=True)

train_size = int(0.8 * len(df))
train_df = df.iloc[:train_size]
test_df = df.iloc[train_size:]

features = ['hour', 'day_of_week', 'month', 'length', 'bus_count', 'message_count', 'segment_id']

X_train = train_df[features]
y_train = train_df['speed']
X_test = test_df[features]
y_test = test_df['speed']

# Train models
lin_reg = LinearRegression()
lin_reg.fit(X_train, y_train)
y_test_pred_lin = lin_reg.predict(X_test)

rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)
y_test_pred_rf = rf.predict(X_test)

gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)
y_test_pred_gb = gb.predict(X_test)

def evaluate(y_true, y_pred):
    mae = np.mean(np.abs(y_true - y_pred))
    mse = np.mean((y_true - y_pred)**2)
    rmse = np.sqrt(mse)
    from sklearn.metrics import r2_score
    r2 = r2_score(y_true, y_pred)
    return {'MAE': mae, 'RMSE': rmse, 'R2': r2}

# Evaluate
metrics = {}
metrics['Linear Regression'] = evaluate(y_test, y_test_pred_lin)
metrics['Random Forest'] = evaluate(y_test, y_test_pred_rf)
metrics['Gradient Boosting'] = evaluate(y_test, y_test_pred_gb)

# Create results CSV
results_df = pd.DataFrame({
    'Model': ['Linear Regression', 'Random Forest', 'Gradient Boosting'],
    'MAE': [m['MAE'] for m in metrics.values()],
    'RMSE': [m['RMSE'] for m in metrics.values()],
    'R2': [m['R2'] for m in metrics.values()]
})
results_df.to_csv('reports/results/traffic_model_results.csv', index=False)

# Plot: Actual vs Predicted
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

# Residuals plot
residuals_lin = y_test - y_test_pred_lin
plt.figure(figsize=(8, 3))
sns.histplot(residuals_lin, bins=30, kde=True)
plt.title('Linear Regression: Residual Distribution')
plt.xlabel('Residual (mph)')
plt.tight_layout()
plt.savefig('reports/figures/residuals_lin.png', dpi=150)

# Feature importance
rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
rf.fit(train_df[features], train_df['speed'])
importances = rf.feature_importances_
indices = np.argsort(importances)[::-1]

plt.figure(figsize=(8, 3))
plt.bar(range(len(features)), importances[indices], align='middle')
plt.xticks(range(len(features)), [str(features[i]) for i in indices])
plt.title('Random Forest: Feature Importance')
plt.tight_layout()
plt.savefig('reports/figures/feature_importance_rf.png', dpi=150)

# Save model
joblib.dump(rf, 'models/traffic_speed_model.pkl')
print('Model saved as models/traffic_speed_model.pkl')

# Print summary
print('Results:')
for mname, m in metrics.items():
    print(f'{mname}: MAE={m["MAE"]:.2f}, RMSE={m["RMSE"]:.2f}, R2={m["R2"]:.3f}')
print('Files saved:')
print('  reports/results/traffic_model_results.csv')
print('  reports/figures/actual_vs_predicted.png')
print('  reports/figures/residuals_lin.png')
print('  reports/figures/feature_importance_rf.png')
print('  models/traffic_speed_model.pkl')