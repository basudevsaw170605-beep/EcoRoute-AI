"""EcoRoute AI - Sustainability-oriented traffic segment decision-support prototype."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from src.route_optimization import normalize_metrics, compute_route_score
from pathlib import Path

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="EcoRoute AI",
    page_icon="🌱",
    layout="wide",
)

st.title("EcoRoute AI")
st.caption("AI/ML-Based Sustainable Urban Route Decision Support")
st.caption(
    "Compare traffic segments using predicted speed, travel time and estimated CO₂ emissions."
)
st.small("AI + Data Science for Sustainable Mobility")

# ---------------------------------------------------------------------------
# Load data once
# ---------------------------------------------------------------------------
@st.cache_data
def load_segment_scores() -> pd.DataFrame:
    """Load the pre-computed segment scores CSV."""
    return pd.read_csv("reports/results/ecoroute_segment_scores.csv")

@st.cache_data
def load_original_data() -> pd.DataFrame:
    """Load the original dataset for reference charts."""
    return pd.read_csv("data/processed/ecoroute_ml_dataset.csv")

segment_scores = load_segment_scores()
df_original = load_original_data()

# ---------------------------------------------------------------------------
# Priority selector
# ---------------------------------------------------------------------------
priority = st.radio(
    "🎯 Choose Your Travel Priority:",
    [
        "Distance Focused",
        "Balanced",
        "Sustainability Focused",
    ],
    index=1,
    help=(
        "Select how to weight distance, travel time, and estimated CO₂ emissions.\n"
        "- Distance Focused: distance 0.60, time 0.30, emission 0.10\n"
        "- Balanced: distance 0.33, time 0.34, emission 0.33\n"
        "- Sustainability Focused: distance 0.10, time 0.30, emission 0.60"
    ),
)

# Map profile display name to column name
profile_col = {
    "Distance Focused": "distance_focused_score",
    "Balanced": "balanced_score",
    "Sustainability Focused": "sustainability_focused_score",
}[priority]

# Display active weights
w = {"Distance Focused": (0.60, 0.30, 0.10),
     "Balanced": (0.33, 0.34, 0.33),
     "Sustainability Focused": (0.10, 0.30, 0.60)}[priority]
st.caption(f"Distance: {w[0]*100:.0f}%  |  Travel Time: {w[1]*100:.0f}%  |  Estimated CO₂: {w[2]*100:.0f}%")

# ---------------------------------------------------------------------------
# Top 5 lowest-score segment options
# ---------------------------------------------------------------------------
st.subheader("🚦 Recommended Segments")

top_5 = segment_scores.nsmallest(5, profile_col)[
    ["segment_id", "street", "direction", "length", "predicted_speed",
     "travel_time_minutes", "estimated_co2",
     profile_col]
].rename(
    columns={
        "length": "Distance (mi)",
        "predicted_speed": "Predicted Speed (mph)",
        "travel_time_minutes": "Travel Time (min)",
        "estimated_co2": "Estimated CO₂ (g)",
        profile_col: "Score",
    }
)

# Format numeric columns
for col in ["Distance (mi)", "Predicted Speed (mph)", "Travel Time (min)", "Estimated CO₂ (g)", "Score"]:
    if col in top_5.columns:
        top_5[col] = top_5[col].round(2)

st.dataframe(top_5, width="stretch", hide_index=True)

# ---------------------------------------------------------------------------
# Why this segment? - dynamic explanation
# ---------------------------------------------------------------------------
st.subheader("🤖 Why Was This Segment Recommended?")

# Use the top segment (lowest score) for the explanation
row = top_5.iloc[0]
dist = row["Distance (mi)"]
speed = row["Predicted Speed (mph)"]
time = row["Travel Time (min)"]
emission = row["Estimated CO₂ (g)"]
score = row["Score"]
profile_name = priority

# Build a factual explanation based on actual values
explanation_parts = [
    f"Under the {profile_name} profile, this segment receives a lower combined score",
    f"because the scoring system places greater importance on ",
]

if profile_name == "Sustainability Focused":
    explanation_parts.append("estimated CO₂ emissions")
elif profile_name == "Distance Focused":
    explanation_parts.append("minimizing distance")
else:
    explanation_parts.append("balancing all three objectives")

explanation_parts.append(
    f" while still considering travel time and distance. "
)
explanation_parts.append(
    f"For this segment: distance = {dist:.2f} mi, "
    f"predicted speed = {speed:.1f} mph, "
    f"travel time = {time:.2f} min, "
    f"estimated CO₂ = {emission:.1f} g, "
    f"score = {score:.4f}."
)

st.info(" ".join(explanation_parts))

# ---------------------------------------------------------------------------
# Visual Analytics
# ---------------------------------------------------------------------------
st.subheader("📊 Segment Comparison Analytics")

col1, col2 = st.columns(2)

# A. Segment Distance vs Estimated CO₂
with col1:
    # Use segment_scores which contains estimated_co2, not df_original
    if "estimated_co2" in segment_scores.columns:
        fig_scatter = px.scatter(
            segment_scores,
            x="length",
            y="estimated_co2",
            color="direction",
            opacity=0.6,
            labels={"length": "Segment Length (miles)",
                    "estimated_co2": "Estimated CO₂ (g CO₂)"},
            title="Segment Distance vs Estimated CO₂",
        )
        st.plotly_chart(fig_scatter, width="stretch")
    else:
        st.warning("Estimated CO₂ data is unavailable for this visualization.")

# B. Predicted Speed vs Travel Time
with col2:
    fig_speed_time = px.scatter(
        segment_scores,
        x="predicted_speed",
        y="travel_time_minutes",
        color="direction",
        opacity=0.6,
        labels={
            "predicted_speed": "Predicted Speed (mph)",
            "travel_time_minutes": "Travel Time (minutes)",
        },
        title="Predicted Speed vs Travel Time",
    )
    st.plotly_chart(fig_speed_time, width="stretch")

# C. Priority Profile Comparison
fig_hist = px.histogram(
    segment_scores,
    x=profile_col,
    nbins=30,
    color="direction",
    opacity=0.7,
    labels={profile_col: "Route Score"},
    title="Route Score Distribution Across Priority Profiles",
)
st.plotly_chart(fig_hist, width="stretch")

# ---------------------------------------------------------------------------
# ML Model Transparency
# ---------------------------------------------------------------------------
with st.expander("🧠 Machine Learning Model"):
    st.markdown(
        "**Task:** Traffic Speed Prediction\n"
        "**Model:** Gradient Boosting Regressor\n"
        "**Training observations:** 620\n"
        "**Split:** Chronological 80/20\n\n"
        "Existing evaluation results:\n"
        "- Linear Regression: MAE 3.52, RMSE 4.68, R² -0.025\n"
        "- Random Forest: MAE 3.64, RMSE 4.75, R² -0.055\n"
        "- Gradient Boosting: MAE 3.64, RMSE 4.59, R² 0.017\n\n"
        "**Note:** The current model is a prototype trained on a limited extracted sample "
        "and should not be interpreted as a city-wide traffic forecasting system."
    )

# ---------------------------------------------------------------------------
# Responsible AI & Limitations
# ---------------------------------------------------------------------------
with st.expander("⚠️ Responsible AI & Limitations"):
    st.markdown(
        "- The ML experiment uses a limited extracted sample of real traffic observations.\n"
        "- Predictions are model outputs and contain uncertainty.\n"
        "- CO₂ values are estimated, not directly measured.\n"
        "- The current prototype compares individual road segments rather than complete "
        "connected routes.\n"
        "- Results are decision-support outputs, not guaranteed outcomes.\n"
        "- User-selected weights influence the recommendation.\n"
        "- The system does not autonomously make decisions.\n"
        "- The prototype does not use sensitive personal information."
    )

# ---------------------------------------------------------------------------
# Data & Methodology
# ---------------------------------------------------------------------------
with st.expander("📁 Data & Methodology"):
    st.markdown(
        "**Source:** Chicago Traffic Tracker — Historical Congestion Estimates by Segment\n"
        "**Dataset period:** June 2024 – April 2026\n"
        "**Prototype extraction:** 620 valid observations\n\n"
        "**Important:** The project uses a limited extracted sample for the current ML prototype. "
        "The 620 observations do NOT represent the complete Chicago dataset.\n\n"
        "**Pipeline:** Real traffic data → ML speed prediction → Travel time estimation → "
        "CO₂ estimation → Multi-objective scoring → User-priority segment recommendation."
    )

# ---------------------------------------------------------------------------
# Footer
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "EcoRoute AI | AI + Data Science for Sustainable Mobility"
)
st.caption(
    "Prototype — results are based on a limited real-data sample."
)