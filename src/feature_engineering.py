"""Feature engineering for EcoRoute AI."""

import pandas as pd
import numpy as np


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Derive useful features for ML models."""

    # Delay ratio: observed speed / free-flow speed estimate
    # Free-flow speed assumed as 80th percentile of observed speeds per route
    if 'average_speed' in df.columns and 'distance' in df.columns and 'travel_time' in df.columns:
        # Free-flow travel time = distance / 80th percentile speed
        free_flow_speed = df['average_speed'].quantile(0.8)
        df['delay_ratio'] = free_flow_speed / df['average_speed'].replace(0, np.nan)

    # Traffic density: volume per km
    if 'traffic_volume' in df.columns and 'distance' in df.columns:
        df['traffic_density'] = df['traffic_volume'] / df['distance'].replace(0, np.nan)

    # Normalize route metrics using min-max scaling
    metric_cols = ['distance', 'travel_time', 'average_speed']
    existing_cols = [c for c in metric_cols if c in df.columns]
    if existing_cols:
        for col in existing_cols:
            min_val = df[col].min()
            max_val = df[col].max()
            if max_val > min_val:
                df[f'{col}_norm'] = (df[col] - min_val) / (max_val - min_val)
            else:
                df[f'{col}_norm'] = 0.5

    # Peak hour indicator (already in data_processing, but ensure consistency)
    if 'peak_hour' not in df.columns:
        if 'hour' in df.columns:
            df['peak_hour'] = ((df['hour'].between(7, 9)) | (df['hour'].between(17, 19))).astype(int)
        elif 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            df['hour'] = df['date'].dt.hour
            df['peak_hour'] = ((df['hour'].between(7, 9)) | (df['hour'].between(17, 19))).astype(int)

    return df


def prepare_features(df: pd.DataFrame, target_col: str) -> tuple:
    """Prepare X and y for ML modeling."""

    # Select numeric columns only
    df = df.select_dtypes(include=[np.number])

    # Separate features and target
    if target_col in df.columns:
        y = df[target_col]
        X_cols = [c for c in df.columns if c != target_col]
        X = df[X_cols]
    else:
        raise ValueError(f"Target column '{target_col}' not found in DataFrame")

    # Simple one-hot encoding for categorical-like numeric columns with few unique values
    # (e.g., congestion_level with 3 values)
    X = pd.get_dummies(X, drop_first=True)

    return X, y