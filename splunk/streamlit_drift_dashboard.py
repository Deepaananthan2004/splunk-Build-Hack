
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from river.drift import ADWIN

# Title and instructions
st.title("📈 Real-Time Behavioral Drift Detection Dashboard")
st.markdown("""
This app simulates user behavior over time and visualizes real-time drift detection using the **ADWIN** algorithm.
You can control the sensitivity of the drift detector using the slider below.
""")

# Drift sensitivity slider
sensitivity = st.slider("Select ADWIN sensitivity (delta)", min_value=0.0001, max_value=0.05, value=0.002, step=0.0005)

# Generate synthetic data
days = 200
drift_day = 120
np.random.seed(42)

engagement = np.concatenate([
    np.random.normal(50, 5, drift_day),
    np.random.normal(70, 5, days - drift_day)
])

dates = pd.date_range(start='2024-01-01', periods=days, freq='D')
df = pd.DataFrame({'date': dates, 'engagement_score': engagement})

# Run ADWIN on the engagement_score
adwin = ADWIN(delta=sensitivity)
drift_indices = []

for i, score in enumerate(df['engagement_score']):
    adwin.update(score)
    if adwin.change_detected:
        drift_indices.append(i)

# Plot the engagement score with drift markers
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['date'], y=df['engagement_score'], mode='lines+markers',
                         name='Engagement Score', line=dict(color='royalblue')))

# Add actual drift reference
fig.add_vline(x=df['date'][drift_day], line=dict(color='orange', dash='dash'), annotation_text="Simulated Drift", annotation_position="top left")

# Add detected drift points
for idx in drift_indices:
    fig.add_vline(x=df['date'][idx], line=dict(color='red', dash='dot'), opacity=0.7)

fig.update_layout(title="ADWIN Drift Detection in User Engagement",
                  xaxis_title="Date",
                  yaxis_title="Engagement Score",
                  template="plotly_white")

st.plotly_chart(fig, use_container_width=True)

# Show drift events table
if drift_indices:
    st.subheader("🔍 Detected Drift Events")
    st.dataframe(df.iloc[drift_indices].reset_index(drop=True))
else:
    st.success("No drift detected with the current sensitivity!")
