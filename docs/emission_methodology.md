# EcoRoute AI — Emission Methodology

## Critical Distinction: Observed → Estimated → Predicted

### Observed Data
- **Definition:** Actual measurements of CO2, NOx, PM2.5, fuel consumption, or vehicle emissions
- **In this dataset:** **NOT AVAILABLE** — the Chicago Traffic Tracker dataset contains no pollution/emission measurements
- **Important:** Never call a derived value "measured pollution" if the dataset does not contain pollution observations

### Estimated Values
- **Definition:** scientifically justified calculations based on established methodologies
- ** basis:** EPA MOVES model, CO2 emission factors, fuel consumption relationships
- **In this project:** CO2 emissions estimated from distance, speed, congestion, and vehicle type using EPA-derived formulas
- **Transparency:** Clearly label as "estimated" and cite the methodology

### Model Predictions
- **Definition:** ML model outputs (regression predictions, classification outputs)
- **In this project:** ML models may predict speed, congestion level, or emissions based on features
- **Transparency:** Distinguish from estimated values; model predictions are interpolative/extrapolative, not measurements

---

## EPA-Based Emission Estimation Formula

Since the dataset contains no direct emission measurements, emissions will be estimated using an established EPA/CO2 methodology. The core formula is:

### Fundamental Relationship

```
emissions_g CO2 = distance_km × emission_factor_g_per_km
```

### Emission Factor by Speed and Congestion

Emission factors (g CO2 per km) vary with vehicle speed and traffic congestion. Based on EPA guidance and typical passenger car data:

| Speed (km/h) | Light Congestion | Medium Congestion | Heavy Congestion |
|-------------|-----------------|-------------------|------------------|
| 0–10 (stop-and-go) | ~180 g/km | ~200 g/km | ~250 g/km |
| 10–30 (slow) | ~130 g/km | ~150 g/km | ~180 g/km |
| 30–50 (moderate) | ~100 g/km | ~110 g/km | ~130 g/km |
| 50–80 (free flow) | ~95 g/km | ~95 g/km | ~100 g/km |
| 80–100 (open flow) | ~110 g/km | ~115 g/km | ~120 g/km |
| 100+ (high speed) | ~130 g/km | ~135 g/km | ~140 g/km |

**Important:** These are approximate values for a typical passenger car. See vehicle type adjustments below.

### Vehicle Type Adjustment

Emission factors are multiplied by vehicle-type multipliers:

| Vehicle Type | Multiplier | Rationale |
|-------------|-----------|-----------|
| Passenger car | 1.0x | Baseline |
| Bus | 2.5x | Heavier engine, more fuel consumption |
| Truck | 3.0x | Significant freight weight, higher emissions |
| Motorcycle | 0.6x | Smaller engine, lower per-km emissions |

### Congestion Multiplier

Traffic congestion increases emissions primarily through idling and stop-and-go patterns:

| Congestion Level | Multiplier | Rationale |
|-----------------|-----------|-----------|
| Light | 1.0x | Free-flow conditions |
| Medium | 1.0x | Typical urban flow |
| Heavy | 1.3x | Stop-and-go, idling, accelerated emissions |

**Formula with all adjustments:**

```
emissions_g CO2 = distance_km × base_emission_factor_g_per_km × congestion_multiplier × vehicle_type_multiplier
```

---

## Required Variables and Their Sources

| Variable | Needed For | Source in Current Dataset | Required Additional Source |
|----------|------------|--------------------------|---------------------------|
| `distance_km` | Emission calculation | NOT AVAILABLE | OpenStreetMap segment geometry, or assumed average (~0.8 km per segment) |
| `average_speed_kmh` | Emission factor lookup | AVAILABLE (SPEED mph × 1.60934) | Convert from `SPEED` column |
| `congestion_level` | Congestion multiplier | DERIVABLE from speed thresholds | `light`: speed > 50 mph, `medium`: 30 < speed <= 50 mph, `heavy`: speed <= 30 mph |
| `vehicle_type` | Vehicle multiplier | NOT AVAILABLE | Assume "passenger_car" (1.0x) for baseline; sensitivity analysis with other types |

**Critical:** 3 of 4 required variables must be obtained from external sources (distance from OSM, vehicle type assumed, congestion derived from speed).

---

## Step-by-Step Estimation Procedure

### Step 1: Prepare Input Variables

```python
# 1. Convert speed from mph to km/h
speed_kmh = speed_mph * 1.60934

# 2. Derive congestion level from speed thresholds
if speed_kmh > 80:  # approximately > 50 mph
    congestion_level = "light"
elif speed_kmh > 50:  # approximately 30–50 mph
    congestion_level = "medium"
else:  # <= 30 mph (~50 km/h)
    congestion_level = "heavy"

# 3. Get distance in km
#    - If OSM geometry available: compute from lineString
#    - If not: use assumed average (e.g., 0.8 km per segment)
distance_km = assumed_distance_km  # e.g., 0.8 km
```

### Step 2: Look Up Base Emission Factor

```python
# Simplified lookup: match speed to emission factor table
def get_base_emission_factor(speed_kmh):
    """Return base emission factor g CO2/km for given speed."""
    if speed_kmh <= 10:
        return 180.0
    elif speed_kmh <= 30:
        return 130.0
    elif speed_kmh <= 50:
        return 100.0
    elif speed_kmh <= 80:
        return 95.0
    elif speed_kmh <= 100:
        return 110.0
    else:
        return 130.0
```

### Step 3: Apply Multipliers

```python
congestion_mult = {"light": 1.0, "medium": 1.0, "heavy": 1.3}.get(congestion_level, 1.0)
vehicle_mult = {"passenger_car": 1.0, "bus": 2.5, "truck": 3.0, "motorcycle": 0.6}.get(vehicle_type, 1.0)

emissions_g = distance_km * base_ef * congestion_mult * vehicle_mult
```

### Step 4: Report with Clear Labeling

```python
print(f"Estimated CO2 emissions: {emissions_g:.2f} grams (estimated, not measured)")
print(f"  Distance: {distance_km:.2f} km")
print(f"  Speed: {speed_kmh:.1f} km/h ({speed_mph:.1f} mph)")
print(f"  Congestion: {congestion_level} (multiplier: {congestion_mult}x)")
print(f"  Vehicle type: {vehicle_type} (multiplier: {vehicle_mult}x)")
print(f"  Base emission factor: {base_ef:.1f} g CO2/km")
```

---

## Distinguishing Emission Types in Outputs

### 1. Emission Estimates (This Project)
```
"The estimated CO2 emissions for Route A are 850g CO2, based on EPA-derived formula using distance, speed, congestion, and passenger car assumptions. This is a model-based estimate, not a direct measurement."
```

### 2. Model Predictions
```
"The ML model predicts 820g CO2 for Route A based on features (speed, distance, congestion). This is a model prediction, distinct from EPA-based estimation."
```

### 3. Actual Measurements (If Available)
```
" measured CO2 emissions: 810g CO2 (direct measurement from tailpipe emissions test)."
```

**Always use language that clearly distinguishes these three categories.**

---

## Sensitivity Analysis for Key Assumptions

Since three of four required variables come from external/assumed sources, run sensitivity analysis:

| Assumption Tested | Values Tested | Impact Reported |
|------------------|---------------|-----------------|
| Segment distance | 0.3 km, 0.5 km, 0.8 km, 1.0 km | Emissions scale linearly with distance |
| Vehicle type | passenger_car, bus, truck | Emissions × 1.0, × 2.5, × 3.0 respectively |
| Congestion level | light, medium, heavy | Emissions × 1.0, × 1.0, × 1.3 respectively |
| Speed bin | adjacent speed categories | Emission factor varies by ~15 g/km per bin |

Report the range of emissions across all sensitivity combinations, e.g.:
```
Emissions range: 624–1,040g CO2 (varying distance 0.3–1.0km, vehicle type passenger car, all congestion levels)
```

---

## Documentation Requirements

Every emission estimate in the project must include:

1. **Formula used:** `emissions = distance × emission_factor × congestion_mult × vehicle_mult`
2. **Distance source:** "OSM geometry" or "assumed 0.8 km per segment" or other
3. **Vehicle type assumption:** "passenger car (baseline)" or other
4. **Congestion derivation:** "from speed thresholds: light > 50 mph, medium 30–50 mph, heavy ≤ 30 mph"
5. **Clear labeling:** "estimated," "model prediction," or "measured"
6. **Sensitivity range:** If assumptions vary, report the range

---

## References

- EPA MOVES Model (Motor Vehicle Emission Simulator): https://www.epa.gov/moves
- EPA CO2 Emission Factors for Highway Vehicles
- Typical passenger car: ~8.9 L/100km fuel consumption → ~20 kg CO2 per gallon → ~5.3 kg CO2 per liter
- Typical emission factors at 50 km/h: ~95 g CO2/km for passenger cars (various sources)