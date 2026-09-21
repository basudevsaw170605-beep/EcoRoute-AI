"""Test Phase 5 route optimization."""
import pandas as pd
import numpy as np
import sys
sys.path.insert(0, 'src')

from route_optimization import normalize_metrics, compute_route_score

# Load data
df = pd.read_csv('data/processed/ecoroute_ml_dataset.csv')
df = df.sort_values('time').reset_index(drop=True)

# Compute travel time in hours
df['travel_time_hours'] = df['length'] / df['speed']

# For emissions proxy, use length
df['emission_proxy'] = df['length']

# Normalize the three metrics using the updated function
# The normalize_metrics function now adds '_norm' suffix
df_norm = normalize_metrics(df, ['length', 'travel_time_hours', 'emission_proxy'])

# The compute_route_score expects columns named 'distance_norm', 'traffic_norm', 'emission_norm'
# Rename columns accordingly:
# - length_norm -> distance_norm (length IS the distance)
# - travel_time_hours_norm -> traffic_norm 
# - emission_proxy_norm -> emission_norm
df_norm = df_norm.rename(columns={
    'length_norm': 'distance_norm',
    'travel_time_hours_norm': 'traffic_norm',
    'emission_proxy_norm': 'emission_norm'
})

print('Normalized columns:', [c for c in df_norm.columns if '_norm' in c])
print()

# Compute route score with balanced weights (0.33, 0.33, 0.33)
scored = compute_route_score(df_norm, 0.33, 0.33, 0.33)
print('Route score head:')
print(scored[['distance_norm', 'traffic_norm', 'emission_norm', 'route_score']].head())