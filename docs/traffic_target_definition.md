# EcoRoute AI — Traffic Target Definition

## Recommended Target: SPEED (Regression)

### Rationale for Choosing SPEED as the Target

The Chicago Traffic Tracker dataset provides `SPEED` as a directly measured (estimated) variable: estimated traffic speed in miles per hour per segment. No other continuous target variable is available in the dataset without derivation or supplementary data. Therefore, SPEED is the most scientifically defensible target for the following reasons:

#### 1. Directly Available
- `SPEED` column is present with values in miles per hour
- No derivation, transformation, or assumption required
- No dependency on external data (e.g., segment distance, road geometry)
- Can be used immediately for model training

#### 2. No Data Gaps or Uncertainty
- Unlike `travel_time` (requires distance) or `congestion_level` (requires threshold definition), `SPEED` requires no additional justification
- No need to assume segment lengths, free-flow speeds, or vehicle types
- No risk of circular reasoning (e.g., defining congestion using the target variable itself)

#### 2.5 Key Advantage: Enables Downstream Derivation
- **Congestion classification** can be derived from predicted speed using objective thresholds:
  - `light`: speed > 50 mph (free flow)
  - `medium`: 30 < speed <= 50 mph (moderate congestion)
  - `heavy`: speed <= 30 mph (heavy congestion)
- **Travel time** can be derived if segment distance becomes available: `travel_time = distance / speed`
- **Emission estimation** can use predicted speed in the EPA-based formula
- Thus, SPEED is a **foundational target** that enables multiple downstream analyses

#### 3. Appropriate ML Problem Type: REGRESSION
- `SPEED` is a continuous numeric variable (range of observed values)
- Predicting *how fast* traffic is moving is a natural regression problem
- Models: Linear Regression, Decision Tree Regressor, Random Forest Regressor, Gradient Boosting Regressor
- Evaluation metrics: MAE (miles per hour error), MSE, RMSE, R²

#### 4. Available Features for Prediction
The following features can be naturally extracted from the dataset to predict SPEED:

| Feature | Source | Notes |
|---------|--------|-------|
| `hour` | `TIME` | Extract from timestamp (0-23) |
| `day_of_week` | `TIME` | Monday=0 to Sunday=6 |
| `weekend` | Derived | Binary (1 if Sat/Sun) |
| `peak_hour` | Derived | Binary (7-9, 17-19) |
| `SEGMENTID` | Direct | Categorical/identifier; treat via embedding or one-hot (if limited unique values) |
| `BUS_COUNT` | Direct | Proxy for traffic volume; more buses → potentially lower speed |
| `MESSAGE_COUNT` | Direct | Data quality proxy; fewer probes → speed estimate less reliable |
| `STREET` | Direct | Can group by street name; different streets have different baselines |
| `STREET_HEADING` | Derived | N/S/E/W; may correlate with direction-specific traffic patterns |

#### 5. Target Definition (Mathematical)
- **Target variable:** `y = SPEED` (miles per hour)
- **Convert to km/h for metric consistency:** `speed_kmh = SPEED * 1.60934`
- **Target range:** Typically 0–60+ mph for urban arterial streets (free flow to standstill)
- **Handling missing values:** Records where `SPEED == -1` have no estimate; these should be excluded from training or imputed

#### 6. Alternative Target Considered but Not Recommended

##### Option A: Congestion Level (Classification)
- **Definition:** Derive categorical labels from `SPEED` thresholds
- **Problem:** Information loss compared to raw speed prediction; arbitrary threshold choices (e.g., why 30 mph vs 25 mph or 35 mph?)
- **When to use:** Only if the project specifically requires congestion classification, not prediction
- **Recommendation:** Derive from SPEED predictions, not as the primary target

##### Option B: Travel Time (Regression)
- **Definition:** `travel_time = distance / speed`
- **Problem:** `distance` is NOT available in the dataset (see Data Gap Analysis). Would require OSM supplementation before this target is viable.
- **When to use:** Phase 3, after segment distances are obtained
- **Recommendation:** Do not use as Phase 2 target

##### Option C: Traffic Volume (Regression)
- **Definition:** Number of vehicles per unit time
- **Problem:** `BUS_COUNT` is a proxy (CTA bus count), not actual traffic volume. `MESSAGE_COUNT` is a data quality metric. Neither represents total vehicle count.
- **When to use:** If the project specifically needs traffic flow measurement
- **Recommendation:** Use `BUS_COUNT` or `MESSAGE_COUNT` as features, not targets

#### 7. Proposed Target Specification

| Attribute | Value |
|-----------|-------|
| **Target name** | `speed_mph` (raw) or `speed_kmh` (metric) |
| **Target type** | Regression (continuous) |
| **Measurement unit** | Miles per hour (raw) or km/h (converted) |
| **Dataset column** | `SPEED` |
| **ML problem** | Regression |
| **Evaluation metric** | MAE, MSE, RMSE (in speed units), R² |
| **Excluded records** | `SPEED == -1` (no estimate available) |
| **Feature set (minimum)** | `hour`, `day_of_week` |
| **Feature set (enhanced)** | `hour`, `day_of_week`, `SEGMENTID`, `BUS_COUNT`, `MESSAGE_COUNT`, `STREET` |

#### 8. Limitations and Mitigations

| Limitation | Mitigation |
|------------|-----------|
| SPEED is an estimate (not measured by physical sensors) | Document as "estimated speed from CTA bus GPS probe data"; consistent with dataset provenance |
| Speed range varies by segment (different streets have different free-flow speeds) | Include `SEGMENTID` or `STREET` as features to capture segment-specific baselines |
| Negative speed values (-1 = no estimate) | Filter out or flag; do not impute with arbitrary values |
| No ground-truth validation data in dataset | Report predictions as relative comparisons (e.g., "Route A predicted speed is 10 mph higher than Route B") rather than absolute truth |
| Chicago-specific data (may not generalize to other cities) | Document dataset scope; results apply to Chicago arterial streets CTA-bus-probed segments |

#### 9. Final Recommendation

**Primary target for Phase 2: `SPEED` (regression in miles per hour)**

This target:
- ✅ Requires no external data or assumptions
- ✅ Is directly available from the dataset
- ✅ Enables derivation of congestion, travel time (if distance added later), and emissions
- ✅ Is appropriate for regression ML models
- ✅ Has a clear evaluation methodology
- ✅ Aligns with the project's goal of traffic analysis for route optimization

**Secondary target (Phase 3, after distance obtained): `travel_time` (regression in minutes)**

This target would become viable after segment distances are obtained from OpenStreetMap, at which point travel time = distance / speed would be a natural target for route optimization.

---

## Documentation of Decision Process

This target was selected through the following reasoning chain:

1. **Identify available variables:** TIME, SEGMENTID, SPEED, BUS_COUNT, MESSAGE_COUNT, STREET, STREET_HEADING
2. **Classify each variable:** Available / Derivable / Requires external / Not available (see `docs/data_gap_analysis.md`)
3. **Identify continuous numeric targets:** Only `SPEED` is directly available as continuous numeric
4. **Evaluate travel time:** Not derivable without distance (gap identified)
5. **Evaluate congestion level:** Derivable from speed, but information loss; better as derived feature than primary target
6. **Evaluate traffic volume:** BUS_COUNT/MESSAGE_COUNT are proxies, not true volume measures
7. **Select SPEED as optimal target:** Directly available, no gaps, enables downstream derivations
8. **Document decision:** In `docs/traffic_target_definition.md` for transparency and reproducibility

---

## References

- Chicago Traffic Tracker dataset description: https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/4g9f-3jbs
- Dataset columns: TIME (Floating Timestamp), SEGMENTID (Number), SPEED (mph), BUS_COUNT (Number), MESSAGE_COUNT (Number), STREET (Text), STREET_HEADING (Text)
- Speed threshold conventions: Typical urban arterial free-flow > 50 mph, moderate 30-50 mph, heavy < 30 mph