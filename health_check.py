"""
Health check endpoint for Google App Engine
"""
import streamlit as st
from datetime import datetime

def health_check():
    """Simple health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "streamlit-app",
        "version": "1.0.0"
    }

# Add to your main Streamlit app
if st._is_running_with_streamlit:
    # This code will only run when accessed via Streamlit
    if st.query_params.get("health") == "check":
        st.json(health_check())
        st.stop()