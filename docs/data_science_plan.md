# EcoRoute AI - Data Science Plan (Steps 4-12)

## STEP 4 — DATA SCIENCE PLAN

### A. Data Collection
Identify realistic sources/types of datasets:

1. **Transportation sensor data** — PeMS (California), traffic loop detector data, or city open data portals
2. **GPS traces** — Floating car data, taxi/GPS traces with speed and timestamp
3. **Weather data** — OpenWeather API or NOAA data (integrated via date/time features)
4. **Vehicle registration/type data** — For emission factor assignments
5. **Road network data** — OpenStreetMap for road characteristics (type, lanes, speed limit)

**Data sources to target:**
- Government transportation departments (open data)
- OpenStreetMap for road graph
- Traffic API services (if prototyping with limited data)
- EPA emission factors for estimation

### B. Data Cleaning
Plan for handling common issues:

- **Missing values:** Impute temporal features (hour, day_of_week) using forward/backward fill; impute numerical features (speed, volume) using median or regression-based imputation. Flag extensive missingness for exclusion.
- **Duplicate records:** Detect and remove exact duplicates; for near-duplicates, keep the most recent or average observations.
- **Inconsistent units:** Convert all distance to km, speed to km/h, time to minutes/hours as needed. Document conversion factors.
- **Outliers:** Use IQR-based filtering or Winsorization for speed and volume. Retain extreme but plausible observations with flags.
- **Categorical variables:** One-hot encode (road type, vehicle type) or ordinal encode (congestion level: light/medium/heavy).
- **Timestamps:** Parse to datetime, extract hour, day_of_week, weekend flag, peak_hour indicator.
- **Invalid observations:** Remove records with negative distance, zero/negative speed, or implausible travel times.

### C. Exploratory Data Analysis
Investigate relationships:

- `distance` vs `travel_time` — linearity, speed profiles
- `congestion_level` vs `travel_time` — impact of congestion on duration
- `congestion_level` vs `emissions` — emission patterns under congestion
- `average_speed` vs `emissions` — speed-emission relationship (typically U-shaped)
- `hour` vs `traffic` — diurnal patterns, peak hours
- `day_of_week` vs `traffic` — weekday vs weekend differences
- `road_characteristics` vs `congestion` — how road type affects flow

### D. Feature Engineering
Derive useful features justified by data:

- `hour` — extracted from timestamp (0-23)
- `day_of_week` — Monday=0 to Sunday=6
- `weekend` — binary (1 if Saturday/Sunday)
- `peak_hour` — binary (1 if hour in [7-9, 17-19])
- `traffic_density` — traffic_volume / distance (vehicles/km)
- `average_speed` — already available, may be derived = distance / travel_time
- `delay_ratio` — observed_speed / free_flow_speed (or observed_travel_time / free_flow_travel_time)
- `normalized_route_metrics` — min-max scaled distance, time, speed for model compatibility
- `is_rush_hour` — binary based on hour and day_of_week

**Only create features that are justified by the available data.**

---

## STEP 5 — ML PROBLEM DEFINITION

### TASK 1 — Traffic Prediction
**Should be: REGRESSION**

**Reasoning:**
- The primary targets (traffic_volume, travel_time, congestion_level as numeric) are continuous or ordinal continuous variables
- We predict *how much* congestion or *how long* travel time is, not discrete categories
- Regression models (Linear Regression, Random Forest Regressor, Gradient Boosting Regressor) are appropriate
- If congestion_level must be classified, it can be treated as ordinal classification later, but the default is regression

**Possible targets:**
- `traffic_volume` — number of vehicles per unit time (regression)
- `congestion_level` — numeric ordinal (regression or ordinal classification)
- `travel_time` — minutes or seconds (regression)

### TASK 2 — Emission Prediction / Estimation
**Approach depends on available data:**

**Case A: Dataset contains actual emission measurements**
- Direct regression problem: predict `emissions_g_co2` from route features
- ML regression model targets estimated emissions

**Case B: Dataset contains no emission data, but has traffic/route features**
- Use scientifically justified estimation formula (EPA/CO2 models)
- Emissions estimated as: `distance * emission_factor(speed, congestion)`
- Emission factors derived from lookup tables or simple ML models

**Case C: Partial data — some emission-related features available**
- ML regression model to predict emissions from: distance, average_speed, traffic_congestion, vehicle_type
- Clearly distinguish: MODEL PREDICTION vs ACTUAL MEASUREMENT

**Always distinguish:**
- ACTUAL MEASUREMENTS (if dataset contains observed emissions)
- MODEL PREDICTIONS (ML model outputs)
- ESTIMATED VALUES (formula-based, not ML-derived)

---

## STEP 6 — MODEL EXPERIMENT STRATEGY

### Regression Models (Task 1 & 2, if regression)
1. **Linear Regression** — baseline, interpretable, fast
2. **Decision Tree Regressor** — captures non-linearities, prone to overfitting
3. **Random Forest Regressor** — ensemble, reduces overfitting, feature importance
4. **Gradient Boosting Regressor** (e.g., XGBoost/LightGBM) — strong performance, careful tuning

### Classification Models (if congestion_level treated as ordinal)
1. **Logistic Regression** — baseline for classified congestion
2. **Decision Tree Classifier**
3. **Random Forest Classifier**
4. **Gradient Boosting Classifier**

**Do not train them yet unless required for a small validation test.**
**Final model selection must be based on measured validation/test performance.**

---

## STEP 7 — EVALUATION PLAN

### For Regression (primary task)
- **MAE** — Mean Absolute Error (interpretability, actual minutes of error)
- **MSE** — Mean Squared Error (penalizes large errors)
- **RMSE** — Root MSE (same units as target)
- **R²** — Coefficient of determination (proportion of variance explained)

**Do not use accuracy alone.**

### For Classification (if applicable)
- **Accuracy** — but always report with
- **Precision** — for the positive/congested class
- **Recall** — for the positive/congested class
- **F1-score** — harmonic mean of precision and recall
- **Confusion Matrix** — detailed error analysis

### Additional considerations
- **Cross-validation** (k-fold, k=5 or 10) for robust performance estimation
- **Overfitting analysis** — compare train vs test performance
- **Train/test leakage** — ensure no temporal or spatial leakage (e.g., same routes in both sets)
- **Class imbalance** — if classification, address imbalanced congestion levels

---

## STEP 8 — ROUTE OPTIMIZATION CONCEPT

**Score(R) formulation:**

After ML models produce predictions for each route R, normalize each metric to [0,1]:

- `d_norm` = normalized distance (min-max scaled)
- `t_norm` = normalized travel time (min-max scaled)
- `c_norm` = normalized congestion (min-max scaled)
- `e_norm` = normalized emissions (min-max scaled)

**Weighted sum score:**

`Score(R) = w_distance × d_norm + w_traffic × t_norm + w_emission × e_norm`

**User priority profiles:**
- **Distance-focused:** w_distance=0.5, w_traffic=0.3, w_emission=0.2
- **Balanced:** w_distance=0.33, w_traffic=0.33, w_emission=0.33
- **Sustainability-focused:** w_distance=0.2, w_traffic=0.3, w_emission=0.5

**The system should explain the trade-offs:**
- Show each route's normalized metrics
- Show how weights affect the final score
- Allow users to adjust priorities

---

## STEP 9 — PARETO OPTIMIZATION (OPTIONAL ADVANCED)

**Purpose:** Identify routes where improving one objective would require worsening another.

**Approach:**
- For a set of routes, compute (distance, travel_time, emissions) for each
- A route is Pareto-optimal if no other route is better in ALL objectives
- Plot routes in 3D or pairwise plots to visualize the Pareto frontier

**Treating as optional:** Only incorporate after the basic ML pipeline is established and validated. Do not implement until core models and evaluation are working.

---

## STEP 10 — AI COMPONENT

**Role:** LLM (e.g., IBM Granite) as explanation layer, NOT model replacement.

**Architecture:**
```
DATA → ML PREDICTION → OPTIMIZATION → NUMERICAL RESULT → AI EXPLANATION
```

**AI use cases:**
- Explain model outputs in natural language (e.g., "Route A is 2 minutes faster but produces 15% more CO2")
- Explain route trade-offs based on user-selected priorities
- Answer sustainability-related questions (e.g., "How much CO2 does this route emit relative to driving X km?")
- Summarize analytical results for the user

**Not used for:**
- Arbitrary route recommendation without ML basis
- Replacing the optimization logic

---

## STEP 11 — RESPONSIBLE AI

Plan for:

- **Transparency:** Clearly distinguish ML predictions from real-world measurements. Display model confidence/uncertainty.
- **Privacy:** No personal location data retained. Route-level analysis only, no individual tracking.
- **Fairness:** Ensure models don't systematically disadvantage certain routes or neighborhoods. Test across different road types and areas.
- **Uncertainty:** Report prediction intervals or confidence ranges, not just point estimates.
- **Prediction limitations:** Explicitly state what the model can and cannot predict. Emission estimates are model-based, not measured.
- **Human decision-making:** The system provides recommendations and trade-off analysis; final route decisions remain with the user.

---

## STEP 12 — README (already created above)