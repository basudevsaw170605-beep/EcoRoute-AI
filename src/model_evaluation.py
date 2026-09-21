"""Model evaluation utilities for EcoRoute AI."""

import numpy as np
import pandas as pd


def evaluate_regression_model(y_true, y_pred, model_name: str = "Model"):
    """Print regression evaluation results."""
    mae = np.mean(np.abs(y_true - y_pred))
    mse = np.mean((y_true - y_pred) ** 2)
    rmse = np.sqrt(mse)
    r2 = 1 - (np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2))

    results = {
        'Model': model_name,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }

    return results


def evaluate_classification_model(y_true, y_pred, model_name: str = "Model"):
    """Compute classification evaluation metrics."""
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix

    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_true, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_true, y_pred, average='weighted', zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=np.unique(y_true))

    results = {
        'Model': model_name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-score': f1,
        'Confusion_Matrix': cm.tolist()
    }

    return results


def compare_models(regression_results: list, classification_results: list = None):
    """Compare multiple model results and return summary."""
    comparison = []

    for result in regression_results:
        comparison.append({
            'Model': result['Model'],
            'MAE': result['MAE'],
            'RMSE': result['RMSE'],
            'R2': result['R2']
        })

    return pd.DataFrame(comparison)