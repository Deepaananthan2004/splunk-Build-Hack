import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time
from river.drift import ADWIN

# --- Streamlit UI ---
st.set_page_config(page_title="Real-Time Drift Detection", layout="wide")

st.title("📊 Real-Time Behavioral Drift Detection Dashboard")
st.markdown("""
Simulates user engagement behavior and continuously monitors **concept drift** using the **ADWIN** algorithm.  
Adjust sensitivity using the slider below and watch the detection update in real time.
""")

# --- Controls ---
sensitivity = st.slider(
    "Select ADWIN sensitivity (delta)",
    min_value=0.0001,
    max_value=0.05,
    value=0.002,
    step=0.0005
)

speed = st.slider(
    "Data stream speed (seconds per update)",
    min_value=0.1,
    max_value=2.0,
    value=0.5,
    step=0.1
)

# --- Initialize variables ---
np.random.seed(42)
adwin = ADWIN(delta=sensitivity)

window_size = 200
drift_day = 120
drift_indices = []

engagement = np.concatenate([
    np.random.normal(50, 5, drift_day),
    np.random.normal(70, 5, window_size - drift_day)
])
dates = pd.date_range(start="2024-01-01", periods=window_size, freq="D")

# --- Stream placeholders ---
chart_placeholder = st.empty()
table_placeholder = st.empty()

# --- Live Stream Simulation ---
data = pd.DataFrame(columns=["date", "engagement_score"])
st.write("📡 Streaming data... press **Stop** (⏹️) or refresh to end.")

for i in range(window_size):
    # Simulate new data point
    new_value = engagement[i]
    new_row = {"date": dates[i], "engagement_score": new_value}
    data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)

    # Update ADWIN detector
    drift = adwin.update(new_value)
    if drift:
        drift_indices.append(i)

    # --- Plot the figure ---
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data["date"],
        y=data["engagement_score"],
        mode="lines+markers",
        name="Engagement Score",
        line=dict(color="royalblue")
    ))

    # Simulated drift day
    fig.add_vline(
        x=str(dates[drift_day]),
        line=dict(color="orange", dash="dash"),
        annotation_text="Simulated Drift",
        annotation_position="top left"
    )

    # Detected drifts
    for idx in drift_indices:
        fig.add_vline(
            x=str(dates[idx]),
            line=dict(color="red", dash="dot"),
            opacity=0.7
        )

    fig.update_layout(
        title="ADWIN Drift Detection (Live Stream)",
        xaxis_title="Date",
        yaxis_title="Engagement Score",
        template="plotly_white",
        showlegend=False
    )

    chart_placeholder.plotly_chart(fig, use_container_width=True)

    # Update drift table
    if drift_indices:
        table_placeholder.subheader("🔍 Detected Drift Events")
        table_placeholder.dataframe(data.iloc[drift_indices].reset_index(drop=True))
    else:
        table_placeholder.info("No drift detected yet...")

    time.sleep(speed)

st.success("✅ Streaming finished.")
