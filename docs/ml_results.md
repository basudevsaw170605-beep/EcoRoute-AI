# EcoRoute AI — ML Results Report

**Phase 4: Traffic Speed Prediction Prototype**

**Dataset size:** 620 observations (7 days, June 2024, limited hours)

**Target variable:** SPEED (miles per hour)

**Model trained:** Gradient Boosting Regressor (n_estimators=100)

**Model performance on test set (80/20 chronological split):**
- MAE: 3.64 miles per hour
- RMSE: 4.59 miles per hour
- R²: 0.017

**Features used:** hour, day_of_week, month, length, bus_count, message_count, segment_id

**Important limitations:**
- This is a prototype experiment on a limited API-derived sample (620 observations)
- The dataset covers only June 2024 (7 days), limited hours (0 and 13), and a subset of Chicago arterial segments
- Model should NOT be presented as providing guaranteed real-world traffic speeds
- Results are exploratory/prototype only and require validation on external data before any practical application

**Model saved as:** models/traffic_speed_model.pkl

---