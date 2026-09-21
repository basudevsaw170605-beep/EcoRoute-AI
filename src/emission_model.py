"""Emission estimation model for EcoRoute AI."""

import numpy as np


def estimate_emissions_epa(distance_km: float, average_speed_kmh: float, 
                           congestion_level: str = "medium", 
                           vehicle_type: str = "passenger_car") -> float:
    """
    Estimate CO2 emissions using a scientifically justified EPA-based formula.

    Emissions g CO2 = distance_km * emission_factor_g_per_km

    Emission factors vary by speed and congestion (based on EPA MOVES/CO2 models):
    - Typical passenger car emission factors g CO2/km at different speeds (approx):
      30 km/h: ~120 g/km
      50 km/h: ~100 g/km
      80 km/h: ~95 g/km
      100 km/h: ~110 g/km (higher due to air resistance)
      120 km/h: ~130 g/km

    Congestion adjustment:
      - "light": 1.0x base emission factor
      - "medium": 1.0x base emission factor
      - "heavy": 1.2-1.5x base emission factor (idling, stop-and-go)

    Vehicle type adjustment:
      - "passenger_car": 1.0x
      - "bus": 2.5x
      - "truck": 3.0x
      - "motorcycle": 0.6x

    Returns estimated emissions in grams of CO2.
    """

    # Base emission factor lookup by speed (g CO2/km)
    emission_factors = {
        30: 120,  # low speed, acceleration
        50: 100,
        60: 98,
        80: 95,
        100: 110,
        120: 130,
    }

    # Find closest speed bin
    if average_speed_kmh in emission_factors:
        base_ef = emission_factors[average_speed_kmh]
    else:
        # Interpolate or use closest
        speeds = sorted(emission_factors.keys())
        closest = min(speeds, key=lambda s: abs(s - average_speed_kmh))
        base_ef = emission_factors[closest]

    # Congestion adjustment
    congestion_multiplier = {
        "light": 1.0,
        "medium": 1.0,
        "heavy": 1.3
    }.get(congestion_level.lower(), 1.0)

    # Vehicle type adjustment
    vehicle_multiplier = {
        "passenger_car": 1.0,
        "bus": 2.5,
        "truck": 3.0,
        "motorcycle": 0.6
    }.get(vehicle_type.lower(), 1.0)

    # Calculate emissions: distance * base_factor * congestion_mult * vehicle_mult
    estimated_emissions_g = distance_km * base_ef * congestion_multiplier * vehicle_multiplier

    return round(estimated_emissions_g, 2)


def estimate_emissions_from_model(travel_time_min: float, distance_km: float,
                                  average_speed_kmh: float, congestion_level: str = "medium",
                                  vehicle_type: str = "passenger_car") -> float:
    """
    Alternative emission estimation based on travel characteristics.

    Uses the relationship: fuel consumption ~ f(speed, congestion)
    Then: CO2 = fuel_consumed * 2.31 kg CO2 / liter (gasoline)
    """

    # Get base emission factor from EPA-style lookup
    base_ef = _get_base_emission_factor(average_speed_kmh)

    # Congestion multiplier
    congestion_mult = {"light": 1.0, "medium": 1.0, "heavy": 1.3}.get(congestion_level.lower(), 1.0)

    # Vehicle type multiplier
    vehicle_mult = {"passenger_car": 1.0, "bus": 2.5, "truck": 3.0, "motorcycle": 0.6}.get(
        vehicle_type.lower(), 1.0)

    # Emissions = distance * emission_factor * congestion * vehicle_multiplier
    estimated_emissions_g = distance_km * base_ef * congestion_mult * vehicle_mult

    return round(estimated_emissions_g, 2)


def _get_base_emission_factor(speed_kmh: float) -> float:
    """Get base emission factor g CO2/km for a given speed."""
    # Simplified EPA-like lookup
    if speed_kmh <= 40:
        return 115.0
    elif speed_kmh <= 80:
        return 95.0
    elif speed_kmh <= 120:
        return 110.0
    else:
        return 125.0


# For direct measurement comparison (if dataset contains actual emissions data)
def compute_prediction_vs_actual_ratio(predicted_g: float, actual_g: float) -> float:
    """
    Compute ratio of model prediction to actual measurement.

    Returns: predicted / actual
    Ratio > 1: model overestimates
    Ratio < 1: model underestimates
    """
    if actual_g == 0:
        return float('inf') if predicted_g > 0 else 0
    return round(predicted_g / actual_g, 4)