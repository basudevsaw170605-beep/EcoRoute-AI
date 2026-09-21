"""Route optimization for EcoRoute AI."""
import numpy as np
import pandas as pd


def normalize_metrics(df: pd.DataFrame, metric_cols: list) -> pd.DataFrame:
    """Normalize metrics to [0, 1] range using min-max scaling.

    Creates new columns with '_norm' suffix containing normalized values.
    """
    df_norm = df.copy()
    for col in metric_cols:
        new_col = col + '_norm'
        min_val = df[col].min()
        max_val = df[col].max()
        if max_val > min_val:
            df_norm[new_col] = (df[col] - min_val) / (max_val - min_val)
        else:
            df_norm[new_col] = 0.5
    return df_norm


def compute_route_score(df: pd.DataFrame, weight_distance: float = 0.33,
                        weight_traffic: float = 0.33, weight_emission: float = 0.33) -> pd.DataFrame:
    """
    Compute multi-objective route score.

    Score(R) = w_distance * d_norm + w_traffic * t_norm + w_emission * e_norm

    All metrics should be normalized to [0, 1] beforehand (via normalize_metrics).
    Lower score = better route (0 = best).
    """

    # Ensure normalized columns exist
    required = ['distance_norm', 'traffic_norm', 'emission_norm']
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing normalized column: {col}. "
                           "Call normalize_metrics first.")

    # Compute weighted score
    df['route_score'] = (
        weight_distance * df['distance_norm'] +
        weight_traffic * df['traffic_norm'] +
        weight_emission * df['emission_norm']
    )

    return df


def find_pareto_optimal_routes(df: pd.DataFrame, obj_cols: list) -> pd.DataFrame:
    """Find Pareto-optimal routes."""
    data = df[obj_cols].values
    is_pareto = np.ones(data.shape[0], dtype=bool)

    for i in range(data.shape[0]):
        dominated = False
        for j in range(data.shape[0]):
            if i == j:
                continue
            if np.all(data[j] <= data[i]) and np.any(data[j] < data[i]):
                dominated = True
                break
        is_pareto[i] = not dominated

    df['pareto_optimal'] = is_pareto
    return df


def route_recommendation(df: pd.DataFrame, priority: str = "balanced") -> dict:
    """Provide route recommendation based on user priority."""

    # Set weights based on priority
    if priority == "distance":
        w_distance, w_traffic, w_emission = 0.60, 0.30, 0.10
    elif priority == "sustainability":
        w_distance, w_traffic, w_emission = 0.10, 0.30, 0.60
    else:  # balanced
        w_distance, w_traffic, w_emission = 0.33, 0.34, 0.33

    # Normalize metrics
    df = normalize_metrics(df, ['distance', 'travel_time', 'emission'])

    # Compute scores
    df = compute_route_score(df, w_distance, w_traffic, w_emission)

    # Find best route (lowest score)
    best_idx = df['route_score'].idxmin()
    best_route = df.loc[best_idx]

    # Get other top routes
    top_routes = df.nsmallest(3, 'route_score')

    explanation = _generate_tradeoff_explanation(best_route, df_scored, priority)

    return {
        'recommended_route': best_route.to_dict(),
        'priority': priority,
        'weights': {'distance': w_distance, 'traffic': w_traffic, 'emission': w_emission},
        'top_routes': top_routes.to_dict('records'),
        'explanation': explanation
    }


def _generate_tradeoff_explanation(best_route, all_routes, priority: str) -> str:
    """Generate natural language explanation of trade-offs."""

    dist = best_route.get('distance', best_route.get('distance_norm', 0))
    time = best_route.get('travel_time', best_route.get('traffic_norm', 0))
    emission = best_route.get('emission', best_route.get('emission_norm', 0))

    metrics = {'distance': dist, 'time': time, 'emission': emission}
    worst_metric = max(metrics, key=metrics.get)

    explanation = f"Based on {priority} priority, Route {best_route.name if hasattr(best_route, 'name') else 'selected'} is recommended.\n\n"

    explanation += f"This route has the lowest combined score with weights optimized for {priority} priority.\n"
    explanation += f"Key metrics: distance, travel time, and emissions.\n"
    explanation += f"The {worst_metric} metric is relatively higher, which is the trade-off "
    f"for optimizing the other objectives under {priority} priority.\n\n"

    if len(all_routes) > 1:
        second_idx = all_routes.nsmallest(2, 'route_score').index[0] if len(all_routes) > 1 else None
        if second_idx is not None:
            second = all_routes.loc[second_idx]
            explanation += f"Alternative route has different trade-offs: may be shorter or faster "
            f"but with different environmental impact.\n"

    return explanation