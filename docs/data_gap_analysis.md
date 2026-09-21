# EcoRoute AI — Data Gap Analysis

## Overview
This document analyzes the availability of required variables for the EcoRoute AI project from the selected dataset (Chicago Traffic Tracker — Historical Congestion Estimates by Segment). For each required variable, the status is classified as:
- **AVAILABLE** — directly in the dataset
- **DERIVABLE** — can be computed from available data (with or without additional data)
- **REQUIRES EXTERNAL DATA** — needs supplementary dataset or API
- **NOT AVAILABLE** — not possible to obtain from any foreseeable source within Phase 2

## Variable Availability Table

| Required Variable | Status | Evidence (from dataset) | Proposed Method |
|-------------------|--------|------------------------|-----------------|
| **Distance** | REQUIRES EXTERNAL DATA | Segment count and IDs only; no segment lengths provided. Segments described as "approximately one-half mile" but exact lengths not specified. | Obtain from OpenStreetMap (OSM) segment geometry. Map SEGMENTID to OSM features via street name and directional heading. Alternative: assume average urban segment length (~0.5 miles = ~0.8 km) for sensitivity analysis. |
| **Speed** | AVAILABLE | `SPEED` column present: estimated traffic speed in miles per hour. Values range; `-1` indicates no estimate. | Directly available as `average_speed` feature. Use for traffic prediction target and emission estimation. |
| **Travel Time** | DERIVABLE (with distance) | Not directly present. Can be calculated as `distance / speed` IF distance is known. | If segment distance obtained from OSM: `travel_time_minutes = distance_km / (speed_mph * 1.60934 / 60)`. Without distance: not derivable. |
| **Traffic / Volume** | DERIVABLE (proxy) | `BUS_COUNT` column: number of CTA buses providing GPS feed. `MESSAGE_COUNT`: number of GPS probes received. Both serve as proxies for traffic volume. | Use `BUS_COUNT` or `MESSAGE_COUNT` as traffic volume proxy. Can also use `SPEED` as inverse proxy (lower speed = higher congestion). |
| **Congestion** | DERIVABLE | Implicit in `SPEED` values. No explicit congestion labels (light/medium/heavy). | Derive congestion level from speed thresholds: `light` (speed > 50 mph), `medium` (30 < speed <= 50 mph), `heavy` (speed <= 30 mph). Or use `delay_ratio = free_flow_speed / observed_speed`. |
| **Emissions** | NOT AVAILABLE | No CO2, NOx, PM2.5, fuel consumption, or vehicle emission measurements in dataset. | Estimate using EPA-style formula (see `docs/emission_methodology.md`). Clearly distinguish: ESTIMATED vs MEASURED. |
| **Road Geometry** | REQUIRES EXTERNAL DATA | No latitude/longitude, no lineString, no polygon. Only `STREET` name and `STREET_HEADING` (N/S/E/W). | Supplement with OpenStreetMap query using `STREET` name and Chicago city boundaries. Could map segments to OSM ways/roads. |
| **Road Characteristics** (lanes, speed limit, type) | REQUIRES EXTERNAL DATA | Not present. `STREET_HEADING` only gives cardinal direction. | Supplement with OpenStreetMap: query by `STREET` name to obtain road class, posted speed limit, number of lanes. |
| **Vehicle Type** | NOT AVAILABLE | Not present in dataset. | Assume single vehicle type (passenger car) for baseline analysis. Run sensitivity analysis with bus/truck factors. Report results per vehicle class. |
| **Weather Conditions** | NOT AVAILABLE | Not present. No temperature, precipitation, or severe weather flags. | Optional supplementary data from NOAA/OpenWeather API. Document as limitation if not included. |
| **Route Destination/Origin** | NOT AVAILABLE | Dataset focuses on segment-level traffic, not origin-destination pairs. | Not supported by this dataset. Would require trip-level data or user-specified routes. |

## Detailed Justification for Each Status

### Distance — REQUIRES EXTERNAL DATA
**Evidence:** The dataset metadata states segments are "approximately one-half mile" of a street in one direction, but no exact lengths are provided. The `SEGMENTID` is an arbitrary unique number with no geometric information. No latitude/longitude or GPS coordinates are present for individual segments.

**Proposed Method:**
1. **Primary:** Query OpenStreetMap (OSM) using `STREET` name and Chicago boundary to find matching road segments. Extract geometry (lineString) and compute length via Haversine or planar distance.
2. **Secondary:** If OSM mapping yields partial results, assume average length of 0.5 miles (≈0.8 km) for unmapped segments and document as approximation.
3. **Tertiary:** For sensitivity analysis, test with multiple assumed segment lengths (0.3 mi, 0.5 mi, 0.7 mi) and report impact on emission estimates and route scores.

**Uncertainty:** OSM mapping success rate depends on Chicago street name coverage. **UNVERIFIED** — may achieve 70-90% segment coverage (estimate based on typical OSM coverage patterns; not empirically verified for this dataset).

### Speed — AVAILABLE
**Evidence:** `SPEED` column is present with values in miles per hour. Description: "Real-time estimated speed in miles per hour. A value of -1 means no estimate is available."

**Proposed Method:**
- Use `SPEED` directly as `average_speed` feature (convert mph to km/h: `km_h = mph * 1.60934`)
- Filter out records where `SPEED == -1` (no estimate available)
- May need to flag records with very low speeds (< 5 mph) as potential data errors

### Travel Time — DERIVABLE (with distance)
**Evidence:** Not directly present in dataset. However, travel time = distance / speed is a fundamental relationship.

**Proposed Method:**
- If distance obtained from OSM: `travel_time_minutes = distance_km / speed_kmph`
- If distance NOT available: travel time cannot be reliably derived. Document as limitation.
- Alternative: Use `BUS_COUNT` or `MESSAGE_COUNT` as indirect proxies for expected travel time patterns (higher volume → potentially longer travel time).

### Traffic / Volume — DERIVABLE (proxy)
**Evidence:** `BUS_COUNT` (number of CTA buses with GPS feed) and `MESSAGE_COUNT` (number of GPS probes) are both present. Dataset description: "Number of buses providing a GPS feed used to estimate congestion" and "Number of GPS probes received(or used) for estimating the speed for that segment."

**Proposed Method:**
- Use `BUS_COUNT` as primary traffic volume proxy
- Use `MESSAGE_COUNT` as data quality indicator (low counts may indicate sparse probe data)
- Normalize both features to [0,1] range for ML model compatibility
- Note: These are probe-based estimates, not counts of all traffic

### Congestion — DERIVABLE
**Evidence:** Congestion is implicit in `SPEED` values. No explicit categorical congestion labels (light/medium/heavy) are provided.

**Proposed Method:**
- Define congestion levels based on speed thresholds (mph):
  - `light`: speed > 50 mph (free flow)
  - `medium`: 30 < speed <= 50 mph (moderate congestion)
  - `heavy`: speed <= 30 mph (heavy congestion / stop-and-go)
- Alternatively, compute `delay_ratio = free_flow_speed / observed_speed` where free_flow_speed could be assumed as posted speed limit or 80th percentile of observed speeds
- For regression tasks, use `SPEED` directly as the target or feature
- For classification tasks, use the above thresholds to create `congestion_level` labels

### Emissions — NOT AVAILABLE
**Evidence:** No CO2, NOx, PM2.5, fuel consumption, or vehicle emission measurements or factors are present in the dataset. The dataset is purely traffic-congestion-focused.

**Proposed Method:**
- Use EPA-based emission estimation formula (see `docs/emission_methodology.md`)
- Required variables for formula: `distance`, `average_speed`, `congestion_level`, `vehicle_type`
- 3 of 4 required variables must be obtained/derived from other sources (distance from OSM, congestion from speed, vehicle type assumed)
- **Critical:** Clearly distinguish ESTIMATED emissions from MEASURED emissions in all outputs and models

### Road Geometry — REQUIRES EXTERNAL DATA
**Evidence:** No latitude/longitude coordinates, no lineString geometries, no polygons. Only `STREET` name (text) and `STREET_HEADING` (N/S/E/W cardinal direction).

**Proposed Method:**
1. **Primary:** Use OpenStreetMap Overpass API or Geofabrik PBF to query road segments by `STREET` name within Chicago city limits. Extract way geometries and compute lengths.
2. **Secondary:** If OSM mapping is successful for a subset of segments, use those for distance calibration and assume average length for remaining segments.
3. **Tertiary:** Document the mapping success rate and limit analysis to segments where geometry was successfully obtained.

### Road Characteristics — REQUIRES EXTERNAL DATA
**Evidence:** Posted speed limit, number of lanes, road type (residential/arterial/freeway) are not present in the dataset.

**Proposed Method:**
1. **Primary:** Query OpenStreetMap using `STREET` name to obtain tags: `maxspeed`, `lanes`, `highway` (road class).
2. **Secondary:** If OSM query returns results for some segments, use those; for remaining segments, assume typical urban arterial values (e.g., 30-40 mph speed limit, 2-4 lanes).
3. **Document:** Report the percentage of segments for which road characteristics were successfully obtained.

### Vehicle Type — NOT AVAILABLE
**Evidence:** No vehicle type classification (passenger car, bus, truck, motorcycle) per observation.

**Proposed Method:**
- **Baseline:** Assume all traffic is passenger cars (`vehicle_type = "passenger_car"`)
- **Sensitivity analysis:** Run models with alternative vehicle types and report impact on emission estimates
- **CTA bus subset:** `BUS_COUNT > 0` may indicate segments with significant bus traffic; could create a separate analysis track for bus-heavy segments
- **Document:** Clearly state assumption of passenger car vehicle type for all emission estimates

### Weather Conditions — NOT AVAILABLE
**Evidence:** No temperature, precipitation, wind, or severe weather variables present.

**Proposed Method:**
- Document as limitation in project scope
- If weather analysis is desired, add optional supplementary data from NOAA Climate Data Online or OpenWeather API
- Restrict any weather-related analysis to days with clear conditions to isolate traffic patterns

### Route Destination/Origin — NOT AVAILABLE
**Evidence:** Dataset is segment-level traffic data, not trip-level or origin-destination data.

**Proposed Method:**
- Not supported by this dataset
- Future work: Could integrate with transit API or user-specified origin-destination pairs
- For now, analysis focuses on segment-level characteristics and multi-segment route construction

## Summary of Data Capabilities

### What This Dataset Enables (Phase 2 Baseline)
- ✅ Traffic speed prediction/regression at segment level
- ✅ Congestion classification/detection from speed thresholds
- ✅ Temporal pattern analysis (hourly, daily, weekday/weekend)
- ✅ Traffic volume proxy analysis (BUS_COUNT, MESSAGE_COUNT)
- ✅ Street-level segmentation and grouping
- ✅ Diurnal and weekly traffic pattern discovery

### What This Dataset Does NOT Enable (Requires Supplementary Data)
- ❌ Exact segment distances (requires OSM or assumption)
- ❌ Travel time computation (requires distance)
- ❌ Emission measurements or direct CO2 data
- ❌ Road geometry or road characteristic details
- ❌ Vehicle type variation per observation
- ❌ Weather condition correlation
- ❌ Origin-destination trip analysis

### Recommended Phase 2 Strategy
1. **Primary:** Use Chicago Traffic Tracker dataset as-is for traffic pattern analysis and speed prediction
2. **Secondary:** Obtain segment distances from OpenStreetMap (parallel task, not blocking)
3. **Tertiary:** Implement EPA-based emission estimation with documented assumptions (distance assumed, vehicle type = passenger car)
4. **Document:** All data gaps and assumptions explicitly in every analysis and model output
5. **Phase 3:** If project continues, integrate OSM data and potentially supplement with additional datasets (fuel consumption databases, emission inventories, etc.)

## Action Items
- [ ] Investigate OpenStreetMap segment mapping for Chicago area
- [ ] Determine segment distance obtainability from OSM
- [ ] Document EPA emission formula and required variables
- [ ] Decide on congestion level threshold definitions
- [ ] Plan sensitivity analysis for key assumptions (segment length, vehicle type)
- [ ] Create data acquisition script for OSM segment distances (Phase 2 optional)