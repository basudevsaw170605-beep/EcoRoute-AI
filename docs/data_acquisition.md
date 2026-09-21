# EcoRoute AI — Data Acquisition Record (Phase 3A)

## Step 1 — Obtain the Real Dataset

### Official Dataset Source
- **Name:** Chicago Traffic Tracker — Historical Congestion Estimates by Segment
- **Data Portal:** https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/4g9f-3jbs
- **Dataset ID:** 4g9f-3jbs
- **API Endpoint:** https://data.cityofchicago.org/resource/qi38-yj8q.json (SATA/SODAQL format)

### Acquisition Attempt

#### SODAQL API Download
- **Attempted:** Python `urllib.request` with `$limit=5, 10, 29, 50, 100`
- **Result:** API returned 29 records but each record was an empty dictionary `{}`
- **Columns:** 0 (all record fields were empty)
- **Error:** The SODAQL API endpoint appears to return structurally empty records in this environment
- **Status:** API download **failed** — cannot retrieve actual data rows through this method

#### Alternative Methods Not Attempted (due to API limitations)
- Direct CSV export from Chicago Data Portal website (requires browser interaction)
- Manual download from the dataset's "Download" button on data.cityofchicago.org
- CKAN API alternative endpoints
- Socrata Open Data API (SODA) client library

### Dataset Not Yet Downloaded

**IMPORTANT:** The real dataset has NOT been saved to `data/raw/`.

- `data/raw/` directory is currently **empty**
- No CSV, Parquet, or JSON file containing actual traffic data is present
- The SODAQL API limitation prevents automatic download in this environment

### Recommended Next Steps for Data Acquisition
1. **Manual download via Chicago Data Portal website:**
   - Visit: https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/4g9f-3jbs
   - Click "Export" → "CSV" or "Download"
   - Save file to `data/chicago_traffic_tracker_historical_2018-2023.csv` (or similar)
   - Then place the file in `data/raw/`

2. **Alternative: Contact data portal administrators**
   - If direct download is blocked, request dataset access through the portal's feedback/contact system

3. **Document the download:**
   - Exact query/filter used
   - Date range selected
   - Number of records downloaded
   - Download date
   - Source URL
   - Any limitations encountered

## Step 2 — Save Raw Data (Pending)

**When the dataset is successfully obtained:**

- **Location:** `data/raw/chicago_traffic_tracker_historical_*.csv` (or `.parquet`, `.json`)
- **Filename convention:** `chicago_traffic_tracker_historical_YYYY-YYYY.csv`
- **Instructions:**
  - Do NOT modify the raw file after acquisition
  - The raw file must remain untouched for reproducibility
  - If the complete dataset is too large, obtain a clearly documented representative subset
  - Document: exact query/filter, date range, number of records downloaded, download date, source URL, limitations

### Until Dataset is Downloaded
- The notebooks in `notebooks/01_data_understanding/` are designed to show "DATASET PRESENT LOCALLY: NO" and provide structure descriptions
- Do NOT fabricate or synthesize data to fill the `data/raw/` directory
- All analysis scripts are on hold until the real dataset is available locally

## Step 3 — Verify the Local Dataset (Pending)

**When the dataset is in `data/raw/`:**

- **Run:** `notebooks/01_data_understanding.ipynb`
- **Must report:**
  - number of rows
  - number of columns
  - column names
  - data types
  - first 10 rows
  - last 10 rows
  - descriptive statistics
  - unique values
  - missing values
  - duplicate rows
  - date range
  - number of unique SEGMENTID values
  - observations per segment
  - SPEED statistics
  - SPEED == -1 count (determine how many; do NOT remove from raw data)

## Step 4 — Data Quality (Pending)

**When the dataset is loaded:**

- Create: `docs/data_quality_report.md`
- Analyze: missing values, duplicate rows, duplicate SEGMENTID+TIME combinations, invalid SPEED values, extreme/outlier SPEED values, timestamp validity, segment coverage, temporal coverage, BUS_COUNT distribution, MESSAGE_COUNT distribution
- All statistics must be calculated from the actual local dataset

## Step 5 — Verify Data Types (Pending)

**When the dataset is loaded:**

- Confirm actual meaning and datatype of: TIME, SEGMENTID, SPEED, BUS_COUNT, MESSAGE_COUNT, STREET, STREET_HEADING, COMMENTS
- Document any additional columns that exist beyond the Phase 2 API sample
- Do not assume the Phase 2 API sample represents every possible column in the complete dataset

## Step 6 — Initial EDA (Pending)

**When the dataset is loaded:**

- Create/edit: `notebooks/02_data_quality_analysis.ipynb` and `notebooks/03_exploratory_data_analysis.ipynb`
- EDA should investigate:
  - Temporal patterns: speed by hour, speed by day of week, weekday vs weekend, peak vs non-peak
  - Segment patterns: speed distribution by segment, number of observations per segment, high/low speed segments
  - Traffic-proxy analysis: BUS_COUNT and MESSAGE_COUNT against SPEED
  - **Important:** Call BUS_COUNT and MESSAGE_COUNT "traffic-related proxy variables" where appropriate, NOT "true traffic volume"

## Step 7 — Important ML Leakage Check (Pending)

**When the dataset is loaded:**

- Investigate whether any feature would leak the target SPEED
- Check: whether BUS_COUNT/MESSAGE_COUNT are measured at the same time as SPEED
- Whether they are available at prediction time
- Whether SEGMENTID/STREET create useful generalizable features
- Whether temporal information causes leakage
- Document reasoning

## Step 8 — Do Not Create Emission Values Yet (Pending)

- Do NOT calculate final emissions during this phase
- First verify: actual distance availability, actual speed distribution, whether external geometry is needed, what emission methodology is scientifically appropriate
- The Phase 2 report already states that actual emission measurements are not available
- **OBSERVED EMISSION ≠ ESTIMATED EMISSION** — Never mix them

## Step 9 — Do Not Build Route Optimization Yet (Pending)

- Do not generate final route recommendations yet
- The traffic dataset is segment-level rather than origin-destination trip data
- First understand the dataset

## Step 10 — ML Readiness Report (Pending)

**When the dataset is loaded and analyzed:**

- Create: `docs/ml_readiness.md`
- Answer:
  1. What is the target? (SPEED — regression)
  2. What are the candidate features? (hour, day_of_week, weekend, peak_hour, SEGMENTID, BUS_COUNT, MESSAGE_COUNT, STREET, STREET_HEADING)
  3. How many usable observations exist? (to be determined from actual data)
  4. How many observations are removed because SPEED == -1? (to be determined)
  5. Are there missing values? (to be determined)
  6. Is the target distribution suitable for regression? (to be determined)
  7. Are there suspicious outliers? (to be determined)
  8. Are there temporal patterns? (to be determined)
  9. Is there possible data leakage? (to be documented)
  10. What train/validation/test strategy should be used? (consider chronological splitting for time-series-like data)

### Important: Train/Test Split Strategy for Time-Series Data

Because this is traffic data with temporal ordering:

- **Random split NOT recommended:** would mix future and past observations, causing data leakage
- **Chronological split recommended:** train on earlier period, test on later period
  - Example: Train on data from Feb 2018 – Aug 2020, Test on Sep 2020 – Sep 2023
  - Or: 80% earliest timestamps for training, 20% latest timestamps for testing
- **Rolling window cross-validation:** another valid approach for time-series data

## Strict Rules Compliance

### DO NOT:
- ✅ fabricate data
- ✅ generate synthetic data
- ✅ fabricate metrics
- ✅ fabricate charts
- ✅ fabricate ML accuracy
- ✅ train final models
- ✅ claim emissions are measured
- ✅ claim traffic volume from BUS_COUNT
- ✅ invent distances
- ✅ invent route geometries
- ✅ build React
- ✅ build Node backend
- ✅ build the final Streamlit application
- ✅ integrate Granite/RAG yet

### DO:
- ✅ Use the real data only
- ✅ Document API limitations honestly
- ✅ Wait for real dataset before ML model training
- ✅ Keep raw dataset untouched
- ✅ Distinguish observed, estimated, and predicted values
- ✅ Clearly mark information that could not be directly verified as UNVERIFIED

## Current Status

| Item | Status |
|------|--------|
| Dataset downloaded to `data/raw/` | ❌ NO — API limitation, manual download needed |
| `data/raw/` contents | Empty |
| Notebook 01 executed | Not executed (dataset not present) |
| Data quality report | Not created (dataset not present) |
| ML readiness report | Not created (dataset not present) |
| Phase 3A complete | In progress — awaiting dataset download |

---
---