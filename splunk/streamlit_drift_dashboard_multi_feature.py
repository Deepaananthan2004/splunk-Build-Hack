import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from river.drift import ADWIN
from datetime import datetime, timedelta

# === Page Config ===
st.set_page_config(page_title="Real-Time Drift Dashboard", layout="wide")

# === Title ===
st.title("📈 Real-Time Behavioral Drift Detection Dashboard")
st.markdown("Detects changes in user behavior patterns using **ADWIN**. Simulated data below.")

# === Parameters ===
NUM_DAYS = 60
SENSITIVITY = st.sidebar.slider("🔧 Drift Sensitivity (ADWIN Delta)", 0.0001, 0.5, 0.01, step=0.005)
DRIFT_DAY = 30
np.random.seed(42)

# === Simulate Data ===
dates = pd.date_range(datetime.today() - timedelta(days=NUM_DAYS), periods=NUM_DAYS)

def generate_feature(name, noise=0.1, drift_magnitude=0.5):
    pre_drift = np.sin(np.linspace(0, 3, DRIFT_DAY)) + np.random.normal(0, noise, DRIFT_DAY)
    post_drift = (np.sin(np.linspace(0, 3, NUM_DAYS - DRIFT_DAY)) + drift_magnitude +
                  np.random.normal(0, noise, NUM_DAYS - DRIFT_DAY))
    return np.concatenate([pre_drift, post_drift])

df = pd.DataFrame({
    "date": dates,
    "session_duration": generate_feature("session_duration", 0.2, 1.0),
    "click_rate": generate_feature("click_rate", 0.1, -1.0),
    "scroll_depth": generate_feature("scroll_depth", 0.15, 0.5)
})

features = [col for col in df.columns if col != 'date']
drift_points = {feature: [] for feature in features}

# === Drift Detection using ADWIN ===
for feature in features:
    adwin = ADWIN(delta=SENSITIVITY)
    for i, value in enumerate(df[feature]):
        drifted = adwin.update(value)
        if drifted:
            drift_points[feature].append(i)

# === Streamlit Tabs ===
tabs = st.tabs([f"📊 {feat.replace('_', ' ').title()}" for feat in features])

for i, feature in enumerate(features):
    with tabs[i]:
        st.subheader(f"Drift Detection for `{feature}`")

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df[feature],
            mode='lines+markers',
            name=feature,
            line=dict(color='royalblue')
        ))

        # Simulated Drift Line (🚫 no annotation_text)
        drift_date = df.loc[DRIFT_DAY, 'date']
        if isinstance(drift_date, pd.Timestamp):
            drift_date = drift_date.to_pydatetime()

        fig.add_vline(
            x=drift_date,
            line=dict(color='orange', dash='dash')
        )

        # Detected Drift Lines (🚫 no annotation_text)
        for idx in drift_points[feature]:
            point_date = df.loc[idx, 'date']
            if isinstance(point_date, pd.Timestamp):
                point_date = point_date.to_pydatetime()

            fig.add_vline(
                x=point_date,
                line=dict(color='red', dash='dot'),
                opacity=0.6
            )

        fig.update_layout(
            title=f"ADWIN Drift Detection - {feature.replace('_', ' ').title()}",
            xaxis_title="Date",
            yaxis_title=feature.replace('_', ' ').title(),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

        # Drift Points Table
        if drift_points[feature]:
            st.markdown("### 🔍 Detected Drift Events")
            drift_df = df.iloc[drift_points[feature]].reset_index(drop=True)
            st.dataframe(drift_df)
        else:
            st.success("✅ No drift detected with the current sensitivity.")

# === Footer ===
st.markdown("---")
st.caption("Built with ❤️ using Streamlit + River + Plotly for Hackathon 2025.")