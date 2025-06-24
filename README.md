# splunk-Build-Hack
📈 Real-Time Drift Detection Dashboard
This project showcases a real-time behavioral drift detection dashboard using Streamlit, River (ADWIN algorithm), and Plotly. Built for the NCT Hackathon 2025, it detects sudden changes in user behavior metrics like session duration, click rate, and scroll depth.

🚀 Live Demo
🌐 Launch on Streamlit Cloud
(replace with your actual URL after deployment)

🔍 What It Does
Simulates time-series behavioral data

Applies ADWIN (Adaptive Windowing) for online drift detection

Visualizes changes with interactive Plotly charts

Allows you to tune sensitivity via a Streamlit sidebar slider

Marks both actual drift and detected drifts

📊 Features
Multi-feature analysis (session_duration, click_rate, scroll_depth)

Drift visualization with red lines and interactive charts

Streamlit tabs for organizing each feature's results

Drift event tables below each plot

🛠 Tech Stack
Tool	Purpose
Streamlit	Web dashboard frontend
River	ADWIN drift detection
Plotly	Interactive time-series plots
Pandas	Data manipulation
NumPy	Synthetic data generation

📦 Setup Instructions
1. Clone this repository
bash
Copy
Edit
git clone : https://github.com/Deepaananthan2004/splunk-Build-Hack/
2. Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
3. Run locally
bash
Copy
Edit
streamlit run streamlit_drift_dashboard_multi_feature.py
📂 File Structure
Copy
Edit
📁 nct-drift-detection/
├── streamlit_drift_dashboard_multi_feature.py
├── requirements.txt
└── README.md
🙌 Credits
Built with ❤️ by [Deepa ananthan AR] for Splunk Build Hackathon 2025.
