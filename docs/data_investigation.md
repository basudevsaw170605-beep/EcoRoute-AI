# EcoRoute AI - Data Requirements Investigation

## Available Real Datasets

### 1. Chicago Traffic Tracker - Historical Congestion Estimates
**Source:** City of Chicago Data Portal
**Coverage:** 2011-2026, 1000+ traffic segments (arterial streets)
**Key columns:**
- `TIME` — Floating timestamp (every 10 minutes)
- `SEGMENTID` — Unique ID for each traffic segment (~0.5 mile road segment in one direction)
- `SPEED` — Estimated traffic speed (mph); -1 means no estimate available
- `BUS_COUNT` — Number of CTA buses providing GPS feed (proxy for traffic volume)
- `MESSAGE_COUNT` — Number of GPS probes received for speed estimation
- `STREET` — Street name
- `STREET_HEADING` — Directional heading (North, South, East, West)

**Suitable for:**
- Traffic prediction: predict speed, congestion, or travel time given segment and temporal features
- Emission estimation: use speed, distance, and congestion to estimate emissions

**Data availability:** Freely available, updated regularly, city open data

---

### 2. FHWA National Performance Management Research Data Set (NPMRDS)
**Source:** Federal Highway Administration
**Coverage:** National Highway System, 52 largest metro areas
**Key metrics:**
- Travel Time Index (TTI): time penalty for a trip on an average day
- Planning Time Index (PTI): reliability measure
- Congested Hours: amount of time when freeways operate < 90% of free-flow speed
- Hours of congestion

**Suitable for:**
- High-level congestion trend analysis
- Validating route-level predictions
- Macro-level emission correlation

**Data availability:** Freely available PDF/reports; raw data access may require registration

---

### 3. Kaggle: Urban Traffic Congestion and Travel Time Analysis
**Note:** This is **synthetic** data designed for analysis practice, not real-world measurements.
**Not recommended** for production ML work, but could be used for prototyping and method development.

---

### 4. Chicago Average Daily Traffic Counts
**Source:** City of Chicago Data Portal
**Coverage:** Traffic count data across city segments
**Suitable for:**
- Validating traffic volume predictions
- Supplementing the Traffic Tracker data

---

## Recommended Dataset for EcoRoute AI

**Primary dataset: Chicago Traffic Tracker - Historical Congestion Estimates by Segment**

**Why this dataset works:**

| Feature | Available in Dataset | ML Use |
|---------|---------------------|--------|
| `TIME` / timestamp | ✓ | Temporal feature extraction (hour, day_of_week) |
| `SEGMENTID` / route identifier | ✓ | Route-level grouping, identify unique routes |
| `SPEED` (mph) | ✓ | Key feature: average_speed; target for regression |
| `BUS_COUNT` / proxy for volume | ✓ | Traffic volume feature |
| `MESSAGE_COUNT` | ✓ | Proxy for data quality/coverage |
| Congestion estimates (implicit in speed) | ✓ | Congestion level classification/regression |

**Derivable features from this dataset:**
- `hour` — from TIME (0-23)
- `day_of_week` — from TIME
- `weekend` — binary (Sat/Sun)
- `peak_hour` — binary (7-9, 17-19)
- `traffic_density` — BUS_COUNT / distance (if distance known per segment)
- `average_speed` — SPEED feature directly
- `delay_ratio` — free_flow_speed / average_speed
- `congestion_level` — derived from speed thresholds (light/medium/heavy)

**For emission estimation, the following are derivable:**
- `distance` — if segment lengths are known (from OpenStreetMap) or assumed constant
- `travel_time` — distance / average_speed
- `average_speed` — directly available as SPEED
- `traffic_congestion` — derived from speed thresholds or BUS_COUNT
- `vehicle_type` — assumed (e.g., "passenger_car") or varied in sensitivity analysis
- **Estimated emissions** — using the EPA-style formula in emission_model.py

---

## Data Gaps and Mitigation Strategy

| Gap | Mitigation |
|-----|-----------|
| **Segment-level distance** | Obtain from OpenStreetMap road segment lengths, or assume average urban segment length (~0.5 miles = ~0.8 km) |
| **Vehicle type variation** | Run sensitivity analysis with different vehicle types (passenger car, bus, truck); report results per vehicle class |
| **Exact CO2 measurements** | Not available in this dataset — use EPA-based estimation formula (as documented in emission_model.py). Clearly distinguish model predictions from actual measurements. |
| **Road characteristics (lanes, speed limit)** | Supplement with OpenStreetMap data query, or use speed itself as proxy for road characteristics |
| **Weather data** | Not in core dataset; can be added later as optional feature. Document as limitation. |

---

## Should Obtain Next

1. **Segment distances** from OpenStreetMap (OSM API query or .pbf file for Chicago area)
2. **Free-flow speed per segment** (posted speed limit from OSM or road class inference)
3. **Optional: Weather data** from NOAA/OpenWeather for days with severe conditions

**Do NOT fabricate data.** If real dataset acquisition proves infeasible within Phase 1, document the specific gaps and target sources for Phase 2. The Chicago Traffic Tracker dataset is a realistic, freely available starting point.

---

## Summary: Minimum Viable Dataset

A minimal dataset supporting ML experiments needs only these columns:
- `timestamp` or `date` + `hour` + `day_of_week`
- `segment_id` or `route_id`
- `speed` (or `average_speed`)
- `bus_count` or equivalent traffic volume proxy

From this minimum, we can engineer features for both traffic prediction and emission estimation.