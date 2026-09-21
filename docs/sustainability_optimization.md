# Sustainability Optimization - EcoRoute AI

## Overview

This document describes the sustainability optimization layer built on the existing EcoRoute AI ML model and dataset. The analysis operates on 620 segment records from the Chicago Traffic Tracker dataset.

## Travel-Time Calculation

**Formula:**
```
travel_time_minutes = length / predicted_speed * 60
```

**Values:**
- `length`: Segment length in miles (from dataset)
- `predicted_speed`: Speed in mph predicted by the Gradient Boosting Regressor model
- `travel_time_minutes`: Computed travel time in minutes

**Sample:** With 620 segments, travel times range from 0.6 to 6.9 minutes, with a mean of 1.3 minutes.

## Emission Estimation Methodology

**Core Formula:**
```
emissions_g CO2 = distance_km * base_emission_factor_g_per_km * congestion_multiplier * vehicle_type_multiplier
```

**Assumptions and Derivations:**

1. **Distance:** Segment length converted from miles to km: `distance_km = length_miles * 1.60934`

2. **Speed-to-Congestion Mapping:**
   - `light`: predicted_speed_mph > 50 mph (speed_kmh > 80 km/h)
   - `medium`: 30 < predicted_speed_mph <= 50 mph (50 < speed_kmh <= 80 km/h)
   - `heavy`: predicted_speed_mph <= 30 mph (speed_kmh <= 50 km/h)

3. **Base Emission Factor (g CO2/km) by speed bin:**
   - speed <= 10 km/h: 180.0 g/km (stop-and-go, high acceleration)
   - 10 < speed <= 30 km/h: 130.0 g/km (slow traffic)
   - 30 < speed <= 50 km/h: 100.0 g/km (moderate flow)
   - 50 < speed <= 80 km/h: 95.0 g/km (free flow, typical)
   - 80 < speed <= 100 km/h: 110.0 g/km (open flow)
   - speed > 100 km/h: 130.0 g/km (high speed, air resistance)

4. **Congestion Multiplier:**
   - light: 1.0x
   - medium: 1.0x
   - heavy: 1.3x (idling, stop-and-go)

5. **Vehicle Type:** Assumed "passenger_car" with multiplier 1.0x. 
   *Sensitivity analysis shows vehicle type has the largest impact on emissions estimates.*

**Full Calculation Pipeline:**
1. Convert observed/predicted speed from mph to km/h
2. Map speed to congestion level and select congestion multiplier
3. Select base emission factor from speed bin lookup
4. Apply: `emissions = distance_km * base_ef * congestion_mult * vehicle_mult`
5. Report as "estimated" (not measured)

**Emission Range:** 48 - 226 g CO2 per segment
**Mean Emissions:** 111 g CO2 per segment

**Critical Labeling:** All emission values are explicitly labeled as "estimated" per the EPA-derived methodology. The dataset contains no direct pollution measurements. See the distinction between observed/predicted/estimated values below.

## Normalization

Before computing route scores, three metrics are normalized to [0, 1] using min-max scaling:

| Metric | Column | Description |
|--------|--------|-------------|
| Distance | `distance_norm` | Normalized segment length (miles) |
| Travel Time | `traffic_norm` | Normalized travel time (minutes) |
| Emissions | `emission_norm` | Normalized estimated CO2 emissions |

Normalization formula: `(value - min) / (max - min)`
If max == min, all values default to 0.5.

## Three User Priority Profiles

### DISTANCE_FOCUSED
- Distance weight: 0.60
- Time weight: 0.30
- Emission weight: 0.10
- *Priority: minimize distance, even at the expense of time and emissions*

### BALANCED
- Distance weight: 0.33
- Time weight: 0.34
- Emission weight: 0.33
- *Priority: equal consideration of all three objectives*

### SUSTAINABILITY_FOCUSED
- Distance weight: 0.10
- Time weight: 0.30
- Emission weight: 0.60
- *Priority: minimize environmental impact, even at the expense of distance and time*

**Score formula:** `Score(R) = w_distance * d_norm + w_traffic * t_norm + w_emission * e_norm`
*Lower score = better route (0 = best).*

## Segment-Option Comparison (vs Complete Route Planning)

**Important Distinction:** This analysis performs segment-option comparison, not complete route planning. The EcoRoute AI dataset contains individual road segments with observed speed and segment-level attributes, but does not contain a complete connected road network with origin-destination paths.

**Why segment-option comparison:**
- The 620-record dataset provides individual segments, not connected routes
- No routing graph is available to compute origin-to-destination paths
- Comparing complete fabricated routes would invent data not present in the dataset
- Segment comparison allows meaningful analysis without fabricating route connections

**Comparison approach:** Each segment is evaluated independently across the three priority profiles, allowing users to see which segments perform best under each priority. This is NOT a route recommendation from point A to point B.

## Limitations of the 620-Record Sample

1. **No complete road network:** Segments are individual, not connected
2. **Speed predictions based on limited features:** Model uses hour, day_of_week, month, length, bus_count, message_count, segment_id
3. **Emission assumptions:** Distance assumed from segment length; vehicle type assumed passenger car; congestion derived from speed thresholds
4. **No actual emission measurements:** All emissions are EPA-model estimates, not measured values
5. **Speed model features:** Features may not capture all factors affecting real-world traffic speed
6. **Urban Chicago bias:** Data from Chicago Traffic Tracker may not generalize to other regions

## Distinction of Value Types

| Value Type | Source | Description |
|------------|--------|-------------|
| **Observed speed** | `speed` column | Actual measured speed from traffic tracker |
| **Predicted speed** | ML model output | Gradient Boosting Regressor prediction based on features |
| **Estimated CO2** | EPA methodology | Calculated emissions from distance, speed, congestion, vehicle type |
| **Distance** | Dataset | Segment length in miles |

## Output Files Generated

- `reports/results/ecoroute_segment_scores.csv` - Segment-level scores for all three profiles
- `reports/figures/segment_distance_vs_emission.png` - Scatter plot of length vs emissions
- `reports/figures/predicted_speed_vs_travel_time.png` - Scatter plot of speed vs travel time
- `reports/figures/route_profile_comparison.png` - Histogram of scores across profiles
- `docs/sustainability_optimization.md` - This documentation

## References

- EPA MOVES Model: https://www.epa.gov/moves
- EPA CO2 Emission Factors for Highway Vehicles
- Typical passenger car: ~8.9 L/100km fuel consumption ~ 20 kg CO2 per gallon ~ 5.3 kg CO2 per liter
- Gradient Boosting Regressor model: models/traffic_speed_model.pkl
- Dataset: data/processed/ecoroute_ml_dataset.csv (620 segments)
