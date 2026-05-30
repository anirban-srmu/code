"""Day 6 demo: minimal dashboard for vision events.
Run: streamlit run streamlit_dashboard.py
"""
import time
import requests
import pandas as pd
import streamlit as st

API = "http://localhost:8000/events"
st.set_page_config(page_title="AI Vision Dashboard", layout="wide")
st.title("AI Vision Event Dashboard")

try:
    data = requests.get(API, timeout=3).json()
    events = data.get("events", [])
except Exception as exc:
    st.error(f"Could not connect to API: {exc}")
    events = []

st.metric("Total events shown", len(events))
if events:
    st.dataframe(events, use_container_width=True)
else:
    st.info("No events yet. Run the object detection/event publisher.")
