# EcoRoute AI

## Project Title
EcoRoute AI: Machine Learning-Based Multi-Objective Sustainable Urban Route Recommendation System

## Problem
Urban transportation contributes significantly to carbon emissions and traffic congestion. Current route recommendation systems typically optimize solely for distance or travel time, ignoring environmental impact and traffic conditions. There is a need for a data-driven framework that balances multiple competing objectives: distance, travel time, traffic congestion, and estimated vehicle emissions.

## Proposed Solution
Develop a machine learning-based multi-objective route recommendation system that:
1. Analyzes alternative routes using distance, travel time, traffic congestion, and emissions data
2. Discovers Pareto-optimal routes where improving one objective requires worsening another
3. Provides personalized route recommendations based on user priorities (distance-focused, balanced, sustainability-focused)
4. Uses transparent ML models with explainable outputs

## Primary SDG
SDG 11: Sustainable Cities and Communities - Make cities and human settlements inclusive, safe, resilient, and sustainable

## Data Science Objectives
- Collect and clean traffic and emissions-related urban routing data
- Perform exploratory data analysis to understand relationships between route metrics
- Engineer features that capture temporal, spatial, and contextual patterns
- Build and validate ML models for traffic prediction and emission estimation

## ML Objectives
- Task 1: Predict traffic congestion/travel time given route and temporal features
- Task 2: Estimate vehicle emissions using travel characteristics and vehicle/road attributes
- Compare multiple regression models (Linear Regression, Decision Tree, Random Forest, Gradient Boosting)
- Select final models based on MAE, MSE, RMSE, and R² evaluation

## AI Objectives
- Use LLM (e.g., IBM Granite) for explaining model outputs and route trade-offs
- Summarize analytical results in natural language
- Answer sustainability-related user questions
- AI operates as an explanation layer ON TOP of ML predictions, not a replacement

## Planned Methodology
1. Data collection from realistic sources (traffic APIs, open data portals, sensor data)
2. Data cleaning and preprocessing (missing values, duplicates, inconsistent units, outliers)
3. Exploratory data analysis (relationships between distance, time, congestion, emissions)
4. Feature engineering (temporal features, derived metrics like delay ratio, traffic density)
5. ML model training and evaluation (train/test split, cross-validation)
6. Multi-objective route scoring and Pareto optimization
7. AI explanation layer integration

## Planned Evaluation
- Regression metrics: MAE, MSE, RMSE, R² for traffic and emission models
- Cross-validation to assess model generalization
- Analysis of overfitting and prediction uncertainty
- Trade-off analysis between competing objectives

## Current Project Status
**Phase 1: Foundation** - Environment inspected, project structure created, data science plan documented.
- Python 3.13.5
- pandas 2.3.2, numpy 2.5, matplotlib 3.10, seaborn 0.13, sklearn 1.9
- Environment inspected, packages verified
- Project structure created
- Data science plan documented
- No fake dataset created
- ML problem definitions established
- Route optimization methodology outlined
- AI role defined (explanation layer, not replacement)
- Responsible AI considerations noted
- Dataset source verified: Chicago Traffic Tracker — Historical Congestion Estimates by Segment
- Data gap analysis completed
- Traffic target defined: SPEED (regression)

**Phase 2: Data Acquisition & Investigation IN PROGRESS**
- Official dataset URL documented: https://data.cityofchicago.org/Transportation/Chicago-Traffic-Tracker-Historical-Congestion-Esti/4g9f-3jbs
- Dataset source verification completed (API sample fetched, column structure confirmed)
- Data gap analysis completed (see docs/data_gap_analysis.md)
- Traffic target definition completed (see docs/traffic_target_definition.md)
- Emission methodology documented (see docs/emission_methodology.md)
- REAL DATASET NOT YET DOWNLOADED to data/raw/
- No ML models trained
- No synthetic data created
- No dashboard built
- IBM Granite/RAG not yet integrated

**Phase 3: ML Model Development (pending)**
- Awaiting real dataset in data/raw/
- Will implement traffic speed prediction models
- Will develop emission estimation models
- Will perform multi-objective route optimization
- Will integrate AI explanation layer

Current status: Phase 2 — Data acquisition and investigation in progress. Real dataset not yet downloaded to data/raw/. Next: download dataset and run data understanding notebook.