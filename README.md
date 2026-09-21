## PROJECT IDENTITY

Project title:
EcoRoute AI � AI/ML-Based Sustainable Urban Mobility Decision Support

Primary focus:
Data Science + Machine Learning + Sustainability

Primary SDG:
SDG 11 � Sustainable Cities and Communities

# EcoRoute AI



## Project title: EcoRoute AI — AI/ML-Based Sustainable Urban Mobility Decision Support

### Primary focus:
Data Science + Machine Learning + Sustainability

### Primary SDG:
SDG 11 — Sustainable Cities and Communities

---

## 1. PROJECT OVERVIEW

EcoRoute AI is an AI/ML-based decision-support prototype that uses real segment-level traffic observations to estimate traffic speed, calculate travel time, and estimate environmental impact. It then compares road segments using configurable multi-objective priorities, allowing users to explore trade-offs between distance, travel time, and estimated CO₂ emissions.

**IMPORTANT:** The current prototype evaluates INDIVIDUAL ROAD SEGMENTS. It is NOT a complete Google Maps-style origin-to-destination routing engine. It does not connect segments into fake routes or provide navigation from point A to point B.

**Terminology:** sustainable mobility decision support, segment recommendation, road-segment comparison, multi-objective optimization.

## 2. PROBLEM STATEMENT

Urban commuters often prioritize shortest distance or travel time, while traffic congestion and environmental impact may also matter. EcoRoute AI explores how traffic prediction, travel-time estimation, estimated emissions, and user-defined priorities can be combined into a transparent decision-support framework.

## 3. SOLUTION

The implemented pipeline:

```text
## Project Pipeline

[1] REAL TRAFFIC DATA
        |
        v
[2] DATA VALIDATION
        |
        v
[3] DATA CLEANING
        |
        v
[4] FEATURE ENGINEERING
        |
        v
[5] TRAFFIC SPEED PREDICTION
        |
        v
[6] TRAVEL TIME ESTIMATION
        |
        v
[7] CO2 EMISSION ESTIMATION
        |
        v
[8] NORMALIZATION
        |
        v
[9] MULTI-OBJECTIVE SCORING
        |
        v
[10] PRIORITY-BASED SEGMENT RECOMMENDATION
        |
        v
[11] STREAMLIT DECISION-SUPPORT DASHBOARD
```

## 4. DATA SOURCE

**Chicago Traffic Tracker — Historical Congestion Estimates by Segment**

- **Dataset ID:** 4g9f-3jbs
- **Official source:** https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/4g9f-3jbs
- **Dataset period:** June 2024–April 2026

The original dataset is much larger than the current prototype sample.

**Current prototype uses:**
- **620 valid real observations**
- **191 unique traffic segments**

**IMPORTANT:** Do NOT claim that 620 observations represent the complete Chicago dataset. The current project uses a limited extracted sample for the prototype.

## 5. DATA FIELDS

Relevant available fields actually used by the project:

- TIME
- SEGMENT_ID
- SPEED (observed speed)
- STREET
- DIRECTION
- FROM_STREET
- TO_STREET
- LENGTH (segment length in miles)
- BUS_COUNT
- MESSAGE_COUNT
- HOUR
- DAY_OF_WEEK
- MONTH
- START_LATITUDE
- START_LONGITUDE
- END_LATITUDE
- END_LONGITUDE

## 6. MACHINE LEARNING

**Task:** Traffic speed prediction / regression

**Models evaluated:**

1. Linear Regression
2. Random Forest
3. Gradient Boosting

**Evaluation method:** Chronological 80/20 train-test split

**Actual results:**

| Model | MAE | RMSE | R² |
|---|---:|---:|---:|
| Linear Regression | 3.52 | 4.68 | -0.025 |
| Random Forest | 3.64 | 4.75 | -0.055 |
| **Gradient Boosting** | **3.64** | **4.59** | **0.017** |

**Selected prototype model:** Gradient Boosting Regressor

**Explanation:** Gradient Boosting had the lowest RMSE and highest R² among the evaluated models.

**IMPORTANT:** The current model is a prototype trained on a limited extracted sample. Its near-zero R² indicates that the current feature/sample configuration has limited predictive strength, so it should not be interpreted as city-wide traffic forecasting.

## 7. SUSTAINABILITY / EMISSION ESTIMATION

The emission methodology is documented in `docs/emission_methodology.md`.

**Critical distinction:**

- **Observed:** Traffic observations such as observed speed (from the dataset)
- **Predicted:** ML-predicted speed (Gradient Boosting Regressor output)
- **Estimated:** CO₂/environmental impact values derived using the project's documented EPA-derived formula

**Explicit statement:** "CO₂ values in the current prototype are estimates, not direct vehicle-level measurements."

## 8. MULTI-OBJECTIVE OPTIMIZATION

The scoring concept combines normalized distance, travel time, and estimated CO₂ using user-selected weights.

**Actual priority profiles:**

| Profile | Distance | Time | Emission |
|---|---:|:---:|---:|
| **Distance Focused** | **0.60** | 0.30 | 0.10 |
| **Balanced** | 0.33 | **0.34** | 0.33 |
| **Sustainability Focused** | 0.10 | 0.30 | **0.60** |

**Explanation:** These profiles allow users to explore trade-offs. Lower score = better route (0 = best).

**IMPORTANT:** The system compares individual road segments, not complete connected-road-network routes. It does not perform full origin-to-destination route optimization.

## 9. STREAMLIT DASHBOARD

The dashboard in `app/app.py` includes the following confirmed features:

- EcoRoute AI dashboard
- Project overview
- Key metrics (620 real observations, 191 unique segments, 3 priority profiles, 3 ML models evaluated)
- How It Works pipeline
- Priority selector (Distance Focused / Balanced / Sustainability Focused)
- Active optimization weights displayed
- Top 5 recommended segments
- Why This Segment dynamic explanation
- Segment comparison analytics
- Distance vs Estimated CO₂ visualization
- Predicted Speed vs Travel Time visualization
- Priority profile comparison
- ML model transparency
- Responsible AI & limitations
- Data & methodology
- Sidebar
- Footer

**Second-stage upgrade features (also documented):**

- Interactive segment map
- Segment explorer
- What-if scenario simulator
- Profile recommendation comparison
- Sustainability insights
- Data science lab
- System architecture

## 10. RESPONSIBLE AI

- Limited prototype sample (620 observations, 191 segments)
- Model uncertainty (near-zero R², limited predictive strength)
- CO₂ values are estimated, not directly measured
- The current prototype compares individual road segments, not complete connected routes
- Results are decision-support outputs, not guaranteed outcomes
- User-controlled priority weights influence recommendations
- The system does not autonomously make decisions
- The prototype does not use sensitive personal information
- Results should not be generalized to all Chicago traffic

**Important statement:** "EcoRoute AI is a decision-support prototype. It does not guarantee the fastest, shortest, or lowest-emission route."

## 11. PROJECT STRUCTURE

```
## Project Structure

EcoRoute-AI/
|
+-- app/
|   +-- app.py
|
+-- data/
|   +-- processed/
|       +-- ecoroute_ml_dataset.csv
|
+-- docs/
|   +-- data_acquisition.md
|   +-- data_investigation.md
|   +-- emission_methodology.md
|   +-- ml_results.md
|   +-- sustainability_optimization.md
|
+-- models/
|   +-- traffic_speed_model.pkl
|
+-- notebooks/
|   +-- 01_data_understanding.ipynb
|   +-- 04_traffic_prediction.ipynb
|
+-- reports/
|   +-- figures/
|   +-- results/
|       +-- ecoroute_segment_scores.csv
|
+-- requirements.txt
+-- README.md
+-- .gitignore
```

## 12. HOW TO RUN

```bash
git clone https://github.com/basudevsaw170605-beep/EcoRoute-AI.git

cd EcoRoute-AI

python -m venv .venv

Windows:
.venv\Scripts\activate

Install:
pip install -r requirements.txt

Run:
streamlit run app/app.py

Then:
http://localhost:8501
```

## 13. RESULTS

- **620** observations
- **191** unique segments
- **3** models evaluated
- Gradient Boosting selected for prototype
- RMSE = 4.59
- R² = 0.017
- Sustainability scoring generates segment-level recommendations under different user priorities

## 14. LIMITATIONS

1. **Limited extracted sample** for current ML prototype (620 observations, 191 segments).
2. **Current model predictive performance is limited** (near-zero R²).
3. **Current system compares individual segments** rather than complete connected routes.
4. **No complete connected road graph** available in the current prototype.
5. **CO₂ values are estimates**, not directly measured vehicle-level data.
6. **No guarantee of future traffic conditions**.
7. **Current results should not be generalized** city-wide.
8. Larger and more representative data would be required for production deployment.

## 15. FUTURE WORK

Possible future work that is NOT yet implemented:

- Larger historical training dataset
- More robust temporal validation
- Connected road-network graph
- Complete origin-destination routing
- Real-time traffic integration
- Better emission modeling
- Uncertainty estimation
- More vehicle types
- Advanced AI explanation layer
- IBM Granite integration for natural-language explanations (labeled as future work)
- Cloud deployment

**Do NOT claim these are already implemented.**

## 16. TECHNOLOGY STACK

- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- Jupyter

Only include libraries that are actually present/used. Do not claim IBM Granite is implemented unless it actually is.

## 17. GITHUB / PROJECT LINK

**GitHub:** https://github.com/basudevsaw170605-beep/EcoRoute-AI

## 18. REMOVE OUTDATED CONTENT

The following statements described the project's **previous state** and have been removed from the main narrative. They are documented here for transparency.

**Deleted outdated statements:**

- **"Phase 1: IN PROGRESS"** / **"Phase 2: IN PROGRESS"** — the project has moved beyond these early planning phases.
- **"Real dataset NOT YET DOWNLOADED"** — the Chicago Traffic Tracker dataset has been acquired and processed.
- **"No ML models trained"** — models are trained and evaluated (3 models, with Gradient Boosting selected as the prototype).
- **"No dashboard built"** — the Streamlit dashboard is fully implemented and running at localhost:8501.
- **"Phase 3: pending"** — ML model development, optimization, and dashboard are complete.
- **"Next: download dataset"** — the dataset has been acquired, cleaned, and featured in the prototype.
- **"AI explanation layer not yet integrated"** — the explanation layer is integrated in the dashboard under "Why This Segment?" and "ML Model".

**Current Implementation** (what the project does today):

- EcoRoute AI is a functional decision-support prototype with a working Streamlit dashboard.
- ML models are trained and evaluated (Linear Regression, Random Forest, Gradient Boosting).
- Sustainability optimization with 3 priority profiles is implemented.
- Segment-level comparison and scoring is operational.
- Responsible AI disclosures are in place.

**Future Work** (what is NOT yet implemented — see section 15):

- Larger historical training dataset
- Connected road-network graph
- Complete origin-destination routing
- Real-time traffic integration
- Better emission modeling
- Uncertainty estimation
- More vehicle types
- Advanced AI explanation layer
- IBM Granite integration for natural-language explanations (labeled as future work)
- Cloud deployment

## 19. FINAL README STYLE

Professional and suitable for:

- GitHub
- 1M1B submission
- College evaluation
- Portfolio

Style guidelines:

- Clear headings
- Concise explanations
- Tables where useful
- Architecture diagram using Markdown
- No excessive emojis
- No exaggerated marketing claims

The README tells a reviewer exactly:

- WHAT the project does
- WHY it matters
- WHAT data was used
- HOW ML is used
- HOW sustainability scoring works
- WHAT results were obtained
- WHAT the dashboard demonstrates
- WHAT limitations remain

---

*EcoRoute AI — AI + Data Science for Sustainable Mobility*