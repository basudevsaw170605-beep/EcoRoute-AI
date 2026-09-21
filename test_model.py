"""Test loading the traffic speed model."""
import joblib
import pandas as pd
import sys
sys.path.insert(0, '.')

# Load the traffic speed model
model = joblib.load('models/traffic_speed_model.pkl')
print('Model type:', type(model))
print('Model params:', model.get_params())

# Check feature names if available
if hasattr(model, 'feature_names_in_'):
    print('Feature names:', model.feature_names_in_)
elif hasattr(model, 'feature_names'):
    print('Feature names:', model.feature_names)

# Load data to see features
df = pd.read_csv('data/processed/ecoroute_ml_dataset.csv')
print('\nData columns:', list(df.columns))