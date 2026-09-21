# EcoRoute AI — Recommended Dataset Strategy (Task 13)

## Overview
After investigating the Chicago Traffic Tracker dataset and identifying critical data gaps, three possible strategies are presented. Based on data quality, ML usefulness, reproducibility, project complexity, sustainability relevance, and ability to complete reliably, **Strategy A is recommended**.

---

## Strategy A: Use Only the Traffic Dataset

### Description
Use the Chicago Traffic Tracker — Historical Congestion Estimates by Segment dataset as the sole data source. No supplementary datasets are integrated during Phase 2.

### What the Project Can Accomplish
- ✅ Traffic speed prediction at segment level (regression target: `SPEED`)
- ✅ Temporal pattern analysis (hourly, daily, weekday/weekend patterns)
- ✅ Congestion classification from speed thresholds
- ✅ Traffic volume proxy analysis (BUS_COUNT, MESSAGE_COUNT)
- ✅ Street-level segmentation and grouping by SEGMENTID/STREET
- ✅ Diurnal and weekly traffic pattern discovery
- ✅ Baseline ML pipeline development (data cleaning, EDA, model training, evaluation)

### What the Project Cannot Accomplish (without supplementary data)
- ❌ Exact distance measurement or travel time computation
- ❌ Emission measurements or EPA-based emission estimates (requires segment distance)
- ❌ Road characteristic details (lanes, speed limits, road type)
- ❌ Vehicle type variation per observation
- ❌ Weather condition correlation
- ❌ Origin-destination trip analysis

### Data Quality Assessment
- **Strengths:** Freely available, city open data; well-documented column meanings; consistent 10-minute sampling; CTA bus GPS probe data source
- **Limitations:** Segment distances not provided; no emission data; no road geometry; no vehicle type variation; Chicago-specific only

### ML Usefulness
- **Adequate for:** Traffic speed prediction, congestion pattern analysis, temporal feature discovery
- **Limited for:** Multi-objective optimization (missing distance and emission metrics)
- **Workaround:** Use predicted speed as proxy for travel time (speed ↓ = time ↑, approximately), but acknowledge the approximation

### Reproducibility
- **High:** Dataset is publicly available; same data can be re-fetched from Chicago Data Portal; processing scripts are defined and reproducible
- **Medium:** OSM distance supplementation (if added later) introduces external dependency

### Sustainability Relevance
- **Moderate:** Supports sustainable transportation analysis through traffic pattern optimization; however, inability to measure/estimate emissions limits sustainability-focused recommendations
- **Workaround:** EPA-based emission estimation with documented assumptions (see `docs/emission_methodology.md`), but clearly labeled as estimated, not measured

### Ability to Complete Reliably
- **High:** All required variables for core analysis are either available or derivable from the dataset; no blocking dependencies on external data acquisition; project can be completed and demonstrated within Phase 2 timeline

### Summary
| Aspect | Rating | Notes |
|--------|--------|-------|
| Data quality | ⭐⭐⭐⭐ | Good for traffic analysis; gaps identified |
| ML usefulness | ⭐⭐⭐⭐ | Strong for speed prediction; limited for full project scope |
| Reproducibility | ⭐⭐⭐⭐⭐ | Dataset freely available; scripts reproducible |
| Complexity | ⭐⭐⭐⭐⭐ | Straightforward; no external data needed |
| Sustainability relevance | ⭐⭐⭐ | Emissions estimable with assumptions, labeled as such |
| Ability to complete | ⭐⭐⭐⭐⭐ | Can complete without blocking dependencies |

---

## Strategy B: Traffic Dataset + One Supplementary Dataset

### Description
Integrate the Chicago Traffic Tracker dataset with one supplementary dataset to address key gaps.

### Recommended Supplementary Dataset(s)

#### Option B1: OpenStreetMap (OSM) — Segment Geometry and Road Characteristics
- **What it provides:** Segment lengths, road geometries, posted speed limits, number of lanes, road class (residential/arterial/freeway)
- **How it's obtained:** Query OSM using `STREET` name within Chicago city boundaries; extract way geometries and compute lengths
- **Gap addressed:** Distance (enables travel time, emission estimates), road characteristics

#### Option B2: NOAA Climate Data Online or OpenWeather API — Weather Data
- **What it provides:** Temperature, precipitation, wind conditions for each observation timestamp
- **How it's obtained:** API calls with TIME parameter; weather conditions at segment level
- **Gap addressed:** Weather-traffic correlation (optional enhancement)

#### Option B3: EPA MOVES Emission Inventory or GREET Fuel Consumption Database
- **What it provides:** Verified emission factors by vehicle type, speed, and congestion level
- **How it's obtained:** Download from EPA website or use established lookup tables
- **Gap addressed:** Emission estimation credibility (replaces assumed factors with verified data)

### What the Project Can Accomplish (with one supplementary)
- ✅ All Strategy A capabilities
- ✅ Exact segment distances (from OSM)
- ✅ Travel time computation (distance / speed)
- ✅ EPA-based emission estimates with verified factors (if Option B3)
- ✅ Road characteristic analysis (if Option B1)
- ❌ Still limited for vehicle type variation per observation
- ❌ Weather correlation (if Option B2 not chosen)
- ❌ Still no direct emission measurements

### Data Quality Assessment
- **Depends on supplementary choice:**
  - OSM: Variable coverage; success rate ~70-90% for Chicago street names (UNVERIFIED estimate)
  - Weather: Depends on API access and data quality
  - EPA factors: Well-established; high credibility

### ML Usefulness
- **Improved:** Distance and emission metrics enable multi-objective route optimization
- **Added complexity:** Data merging, alignment, and integration logic

### Reproducibility
- **Medium:** Depends on supplementary dataset availability; OSM queries may have variable success; APIs may have rate limits or costs

### Sustainability Relevance
- **Improved:** If OSM + EPA factors chosen, emission estimates become more credible; still labeled as estimated, not measured

### Ability to Complete Reliably
- **Medium-Low:** Adds external dependencies (OSM query success, API access, data licensing); may block progress if supplementary data acquisition proves difficult

### Summary
| Aspect | Rating (with OSM) | Rating (with EPA factors) |
|--------|------------------|--------------------------|
| Data quality | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| ML usefulness | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Reproducibility | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Complexity | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| Sustainability relevance | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Ability to complete | ⭐⭐⭐ | ⭐⭐⭐⭐ |

---

## Strategy C: Traffic Dataset + Road/Network + Environmental/Emissions Data

### Description
Integrate three data layers: (1) Chicago Traffic Tracker, (2) OpenStreetMap road network, (3) Environmental/emissions dataset.

### What Each Layer Provides
1. **Chicago Traffic Tracker:** Speed, congestion, temporal data for 1000+ segments
2. **OpenStreetMap:** Segment geometries, distances, road characteristics (lanes, speed limits, road type)
3. **Environmental dataset:** CO2 measurements, fuel consumption rates, emission factors by vehicle type and region

### What the Project Can Accomplish
- ✅ Full multi-objective optimization: distance, travel time, congestion, emissions
- ✅ Comprehensive emission analysis with measured/verified data
- ✅ Road network analysis and route graph construction
- ✅ Vehicle type-specific emissions
- ✅ Weather-traffic-emission correlation (if weather data added)
- ✅ Advanced Pareto-optimal route analysis

### Data Quality Assessment
- **Strengths:** Most comprehensive; verified data where available
- **Limitations:** 
  - OSM query complexity and coverage uncertainty
  - Environmental dataset availability and access
  - Data alignment across different formats and projections
  - Potential data silos and integration challenges

### ML Usefulness
- **Maximum:** All ML tasks supported with complete data
- **Added value:** Can train emission prediction models, not just estimation

### Reproducibility
- **Lower:** Multiple external dependencies; data acquisition may vary; integration logic adds complexity

### Sustainability Relevance
- **High:** Direct emission measurements or highly credible estimates; full sustainability analysis possible

### Ability to Complete Reliably
- **Lowest:** Highest complexity; multiple external dependencies; longest time to complete; risk of scope creep

### Summary
| Aspect | Rating |
|--------|--------|
| Data quality | ⭐⭐⭐⭐ (depends on sources) |
| ML usefulness | ⭐⭐⭐⭐⭐ |
| Reproducibility | ⭐⭐⭐ |
| Complexity | ⭐ |
| Sustainability relevance | ⭐⭐⭐⭐⭐ |
| Ability to complete | ⭐⭐ |

---

## Recommendation: Strategy A

### Reasoned Recommendation

**Strategy A (Use only the traffic dataset) is recommended** based on the following criteria:

#### 1. Data Quality
- The Chicago Traffic Tracker dataset is high-quality for its intended purpose (traffic congestion monitoring)
- All gaps are documented and understood; no hidden or unknown data issues
- Strategies B and C introduce unverified data sources (OSM query success rates, environmental dataset availability) that could delay or compromise the project

#### 2. ML Usefulness
- Strategy A enables core ML work: traffic speed prediction, model training, evaluation
- The target variable (SPEED) is directly available with no derivation required
- Strategies B and C add complexity that could distract from the core ML pipeline
- Multi-objective optimization can use speed as a proxy for travel time with explicit documentation of the approximation

#### 3. Reproducibility
- Strategy A is fully reproducible: same dataset from public source, same processing scripts
- The dataset is freely available and can be re-fetched at any time
- No API keys, rate limits, or external dependencies blocking progress

#### 4. Project Complexity
- Strategy A keeps the project focused and manageable
- All Phase 2 tasks can be completed within a reasonable timeline
- Strategies B and C risk scope creep; the project could extend indefinitely as more data sources are sought
- The simple architecture (DATA → ML PREDICTION → OPTIMIZATION → RESULT → AI EXPLANATION) is maintained

#### 5. Sustainability Relevance
- Emission estimates can be produced with documented assumptions (see `docs/emission_methodology.md`)
- Clearly labeled as "estimated" rather than "measured" — transparent and honest
- The project can still contribute to sustainable transportation analysis through traffic pattern optimization and speed-based insights (e.g., "slower speeds → higher emissions per km, suggesting routes that maintain moderate speeds")
- If sustainability is the primary focus in Phase 3, supplementary data can be added then

#### 5. Ability to Complete Reliably
- **Highest probability of success** within the Phase 2 timeline
- No blocking dependencies; all required analysis can be done with available data
- The project can be demonstrated and evaluated without waiting for external data acquisition
- If the project proves valuable, supplementary data can be integrated in Phase 3 as a natural extension

### Implementation Plan for Strategy A

#### Phase 2 (Current) — Complete
- ✅ Dataset source verified
- ✅ Data gap analysis completed
- ✅ Traffic target defined (SPEED regression)
- ✅ Emission methodology documented (with assumptions)
- ✅ No data downloaded to data/raw/ (intentional — awaiting Phase 3 or user action)

#### Phase 3 (Recommended Next Steps)
1. **Download the real dataset** to `data/raw/` (Chicago Traffic Tracker CSV/Parquet)
2. **Run notebook 01_data_understanding.ipynb** to inspect the loaded dataset
3. **Implement traffic speed prediction models** using the `src/traffic_model.py` module
4. **Implement emission estimation** using the EPA formula from `docs/emission_methodology.md` with documented assumptions
5. **Conduct EDA and feature engineering** using `src/feature_engineering.py`
6. **Evaluate models** using `src/model_evaluation.py` (MAE, MSE, RMSE, R²)
7. **Implement multi-objective route scoring** using `src/route_optimization.py` with speed-based time proxy
8. **Integrate AI explanation layer** (Phase 3 optional, using LLM for model output explanations)
9. **Document all assumptions and limitations** transparently in all outputs

#### Key Principles for Phase 3 Upgrades (if/when supplementary data is added)
- If OSM segment distances are added: recompute travel time = distance / speed; update emission estimates
- If verified emission data is added: replace EPA-based estimates with measured values; update documentation
- If vehicle type data is added: run sensitivity analysis; report results per vehicle class
- Always: distinguish observed, estimated, and predicted values; never fabricate or imply measurements that weren't taken

### Conclusion
Strategy A balances data quality, ML usefulness, reproducibility, complexity, sustainability relevance, and reliability. It allows the project to be completed and demonstrated within Phase 2 while leaving natural extension points for Phase 3. Strategies B and C add valuable capabilities but introduce dependencies that risk delaying or complicating project completion. The EcoRoute AI project can deliver meaningful traffic analysis and route optimization insights with Strategy A, and supplementary data can be integrated later if the project scope expands.

---
---