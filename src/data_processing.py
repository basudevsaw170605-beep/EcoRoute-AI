"""Data processing utilities for EcoRoute AI."""

import pandas as pd
import numpy as np


def load_raw_data(path: str) -> pd.DataFrame:
    """Load raw dataset from CSV path."""
    df = pd.read_csv(path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw data: handle missing values, duplicates, invalid observations."""

    # Remove duplicate records
    df = df.drop_duplicates()

    # Remove invalid observations (negative distance, zero/negative speed)
    df = df[(df['distance'] > 0) & (df['average_speed'] > 0)]

    # Handle missing values
    # Temporal features: fill using forward fill
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        df['hour'] = df['date'].dt.hour
        df['day_of_week'] = df['date'].dt.day_name()

    # Impute numerical columns with median
    num_cols = df.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        df[col] = df[col].fillna(df[col].median())

    return df


def extract_temporal_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract hour, day_of_week, weekend flag, and peak_hour from timestamps."""

    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df['hour'] = df['date'].dt.hour
        df['day_of_week'] = df['date'].dt.day_of_week  # 0=Monday, 6=Sunday
        df['weekend'] = df['day_of_week'].isin([5, 6]).astype(int)  # 5=Sat, 6=Sun
        df['peak_hour'] = ((df['hour'].between(7, 9)) | (df['hour'].between(17, 19))).astype(int)

    return df