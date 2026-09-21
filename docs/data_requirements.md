# EcoRoute AI - Data Science Plan

## STEP 3 — DATA REQUIREMENTS

### Traffic Prediction Data Requirements
The following features are needed to support legitimate ML experiments for traffic prediction:

**Required features:**
- `date` / timestamp
- `day_of_week` (derived from date)
- `hour` (derived from timestamp)
- `route_id` / road identifier
- `distance` (km or miles)
- `traffic_volume` (vehicles per hour)
- `average_speed` (km/h or mph)
- `travel_time` (minutes or seconds)
- `congestion_level` (ordinal or categorical)
- `road_characteristics` (road type, lanes, speed limit)

**Target variables:**
- `traffic_volume` (regression)
- `congestion_level` (ordinal classification or regression)
- `travel_time` (regression)

### Emission Estimation Data Requirements
The following features support emission estimation:

**Required features:**
- `distance` (km or miles)
- `travel_time` (minutes or seconds)
- `average_speed` (km/h or mph)
- `traffic_congestion` (level or density)
- `vehicle_type` (passenger car, bus, truck, motorcycle)
- `fuel_consumption` (liters/100km or mpg) — if available
- `emission_factor` — if available (g CO2/km)

**Target variables:**
- `emissions_g_co2` (direct measurement, if available)
- `estimated_emissions` (model-based estimation)

**Note:** If actual emission measurements are not available, emissions will be estimated using scientifically justified formulas based on the EPA/CO2 emission models that relate distance, speed, and congestion to fuel consumption and CO2 output.

### What Type of Dataset We Should Obtain
- **Ideal:** Real traffic sensor data from a city's transportation department, combined with emission factors
- **Acceptable:** Publicly available traffic datasets (e.g., PeMS, TaxiBike, carriageway sensor data) with timestamp, speed, and volume
- **Minimum:** Synthetically generated data based on established traffic/emission models, validated against real patterns

**Do NOT:** Fabricate a dataset just to make the project appear complete. If a suitable real dataset is not immediately available, clearly document what data is missing and what sources to target.

---

## STEP 3 — DATA REQUIREMENTS (SUMMARY)
- Traffic features: date, day_of_week, hour, route_id, distance, traffic_volume, average_speed, travel_time, congestion_level, road_characteristics
- Emission features: distance, travel_time, average_speed, traffic_congestion, vehicle_type, fuel_consumption/emission_factor
- Target: traffic_volume / congestion_level / travel_time (regression) AND emissions_g_co2 (estimation)
- Dataset source: real traffic sensor data, open data portals, or established models — NOT fabricated