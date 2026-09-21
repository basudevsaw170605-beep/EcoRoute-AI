# EcoRoute AI — Dataset Source Verification

## Official Dataset Name
**Chicago Traffic Tracker — Historical Congestion Estimates by Segment**

## Official URL / API Endpoint
**Data Portal:** https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/4g9f-3jbs
**Dataset ID:** 4g9f-3jbs
**API Endpoint (SATA):** https://data.cityofchicago.org/resource/qi38-yj8q.json
**Metadata/Explore Page:** https://data.cityofchicago.org/d/qi38-yj8q

## Dataset Description
The Chicago Traffic Tracker estimates traffic congestion on Chicago's arterial streets (non-freeway streets) in real-time by continuously monitoring and analyzing GPS traces received from Chicago Transit Authority (CTA) buses. This dataset contains historical estimated congestion for over 1,000 traffic segments, starting in approximately February 2018 and ending September 2023 (older records August 2011 – May 2018). Newer records are available in the 2024-2026 version of the dataset.

**Two types of congestion estimates are produced every 10 minutes:**
1. **By Traffic Segments:** Observed speed typically for one-half mile of a street in one direction of traffic. Traffic segment level congestion is available for about 300 miles of principal arterials.
2. **By Traffic Region:** Average traffic condition for all arterial street segments within a region. A traffic region is comprised of two or three community areas with comparable traffic patterns. 29 regions cover the entire city (except O'Hare airport area).

## Data License / Accessibility
- **Access Level:** Public
- **Cost:** Free
- **Update Frequency:** Regular updates (dataset last updated August 6, 2026) **VERIFIED** — from data portal metadata
- **Bulk Download:** Available via SATA (Soql/Atrad API) or CSV export from the data portal
- **API Access:** SodaQL/Soap2 available via the resource endpoint

## Date Range Actually Available
- **Historical records:** Approximately February 2018 – September 2023 **UNVERIFIED** — date range from dataset portal description; not independently verified from raw data
- **Older records:** August 2011 – May 2018 (separate dataset) **UNVERIFIED** — refers to older version of the dataset; exact coverage not verified
- **Current/recent:** 2024 – 2026 (most recent estimates) **UNVERIFIED** — from dataset portal; actual latest slice not accessed
- **Sampling frequency:** Every 10 minutes per segment — as described in dataset metadata

## Record Count
- **~1,000+ traffic segments** (arterial streets in Chicago) **UNVERIFIED** — API returned sample of 5 records; exact segment count not independently verified
- **Multiple observations per segment** (one every 10 minutes) — as described in dataset metadata
- **Total records:** Millions of row-time observations across the date range **UNVERIFIED** — estimate based on dataset description; exact count not verified

## Column Names and Meanings

| Column Name | Data Type | Description | Notes |
|-------------|-----------|-------------|-------|
| `TIME` | Floating Timestamp | Date and time corresponding to congestion estimate | `last_update` in API field name |
| `SEGMENTID` | Number | Unique ID for each segment | Represents ~0.5 mile road segment in one direction |
| `SPEED` | Number | Estimated traffic speed in miles per hour | `-1` means no estimate available |
| `BUS_COUNT` | Number | Number of buses providing a GPS feed used to estimate congestion | Proxy for traffic volume |
| `MESSAGE_COUNT` | Number | Number of GPS probes received (or used) for estimating the speed for that segment | Data quality proxy |
| `STREET` | Text | Street name of the traffic segment | |
| `STREET_HEADING` | Text | Position of the segment in the address grid (North, South, East, or West) | |
| `COMMENTS` | Text | Additional comments | |

## Important Notes About SEGMENTID
- SEGMENTID represents a **unique arbitrary number** for each traffic segment
- Each segment is approximately **one-half mile** of a street in **one direction** of traffic
- About 300 miles of principal arterials have segment-level coverage
- Segments are derived from CTA bus GPS probe data
- SEGMENTID does NOT directly provide: road name, latitude, longitude, geometry, or segment length
- Different segments may overlap or be adjacent; SEGMENTID is primarily for identification, not geography

## Data Structure Summary
- **Spatial coverage:** Chicago arterial streets (non-freeway)
- **Temporal coverage:** 2011-2026 (various segments have different coverage within this range)
- **Temporal granularity:** 10-minute intervals
- **Observation universe:** Each segment-timestamp combination is a separate record
- **Key variables for ML:** TIME, SEGMENTID, SPEED, BUS_COUNT, MESSAGE_COUNT

## Variables NOT in This Dataset (Critical Gaps)
The following variables needed for EcoRoute AI are **NOT directly available** in the Chicago Traffic Tracker dataset:

1. **Segment distance/length:** Not provided. Segments are approximately 0.5 miles but exact lengths not specified.
2. **Travel time:** Not directly available. Would need distance ÷ speed (requires segment distance).
3. **CO2 / emissions measurements:** Not available. Would require EPA-based estimation formula.
4. **Road characteristics (lanes, speed limit, road type):** Not available. Would need OpenStreetMap supplementation.
5. **Vehicle type:** Not available. Would need to assume (e.g., passenger car) or do sensitivity analysis.
6. **Actual congestion labels (light/medium/heavy):** Implicit in speed values but not explicitly labeled.
7. **Weather data:** Not available. Would need external API (NOAA, OpenWeather).

## Variables AVAILABLE in This Dataset
The following variables can support ML experiments directly:

1. **TIME** — Temporal feature; extract hour, day_of_week, weekend, peak_hour
2. **SEGMENTID** — Route/segment identifier; group observations by unique segment
3. **SPEED** (mph) — Key feature: average_speed; can be target for regression
4. **BUS_COUNT** — Proxy for traffic volume
5. **MESSAGE_COUNT** — Proxy for data quality / GPS probe coverage
6. **STREET** — Street name (can be used for grouping/identification)
7. **STREET_HEADING** — Directional heading (N, S, E, W)

## Derivable Variables (With Additional Data)
The following variables can be derived IF supplementary data is obtained:

1. **Distance:** From OpenStreetMap segment geometry (if segment IDs can be mapped to OSM features)
2. **Travel time:** `distance / speed` (requires segment distance)
3. **Congestion level:** Derived from speed thresholds (e.g., < 30 mph = heavy, 30-50 = medium, > 50 = light)
4. **Traffic density:** `BUS_COUNT / distance` (requires segment distance)
5. **Delay ratio:** `free_flow_speed / observed_speed` (requires free-flow speed assumption)

## Summary: What This Dataset Can Support
- ✅ Traffic speed prediction (regression)
- ✅ Congestion level classification (from speed)
- ✅ Traffic volume proxy (BUS_COUNT)
- ✅ Time-of-day and day-of-week pattern analysis
- ✅ Route-segment grouping and analysis
- ❌ Exact distance measurement (requires OSM)
- ❌ Travel time (requires distance)
- ❌ Emissions (requires EPA formula)
- ❌ Road characteristics (requires OSM or other source)