import streamlit as st
from anthropic import Anthropic
import os
from datetime import datetime
from dotenv import load_dotenv
import httpx
import json
from typing import Optional, List, Dict, Any
import re
import time
import base64
from PIL import Image
import PyPDF2
import io
from audio_recorder_streamlit import audio_recorder
try:
    import speech_recognition as sr
except ImportError:
    sr = None
import subprocess
import numpy as np

# Load environment variables
load_dotenv()

# ULTRA MODERN PROFESSIONAL THEME
st.set_page_config(
    page_title="Izza MD PhD - Medical Intelligence",
    page_icon="⚕️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ULTRA MODERN CSS DESIGN SYSTEM
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Main App Container */
    .stApp {
        background: linear-gradient(180deg, #ffffff 0%, #f8f9fa 100%);
    }
    
    /* Header Section */
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 3rem 2rem;
        border-radius: 0 0 30px 30px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
    }
    
    .app-title {
        color: white;
        font-size: 3.5rem;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .app-subtitle {
        color: rgba(255,255,255,0.95);
        font-size: 1.2rem;
        font-weight: 300;
        margin-top: 0.5rem;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    
    /* Modern Card Design */
    .modern-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid rgba(0,0,0,0.05);
        margin: 1.5rem 0;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .modern-card:hover {
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }
    
    /* Professional Alert Box */
    .medical-alert {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 2rem 0;
        box-shadow: 0 8px 24px rgba(238, 90, 36, 0.25);
        border-left: 5px solid #c44133;
    }
    
    .medical-alert h4 {
        margin: 0 0 0.75rem 0;
        font-weight: 600;
        font-size: 1.1rem;
        letter-spacing: 0.5px;
    }
    
    .medical-alert p {
        margin: 0;
        line-height: 1.6;
        font-size: 0.95rem;
        opacity: 0.98;
    }
    
    /* Modern Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 4px 14px rgba(102, 126, 234, 0.4);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
    }
    
    /* Primary Button Style */
    .stButton > button[data-baseweb="button"][kind="primary"] {
        background: linear-gradient(135deg, #48c774 0%, #3ec46d 100%);
        box-shadow: 0 4px 14px rgba(72, 199, 116, 0.4);
    }
    
    /* Text Input Fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #e0e6ed;
        padding: 0.75rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #f8f9fa;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    /* Text Area */
    .stTextArea > div > div > textarea {
        border-radius: 12px;
        border: 2px solid #e0e6ed;
        padding: 1rem;
        font-size: 1rem;
        background: #f8f9fa;
        transition: all 0.3s ease;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        background: white;
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #ffffff 100%);
        border-right: 1px solid #e0e6ed;
    }
    
    .sidebar .sidebar-content {
        padding: 2rem 1rem;
    }
    
    /* Metrics Cards */
    [data-testid="metric-container"] {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e0e6ed;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    
    [data-testid="metric-container"]:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }
    
    /* Chat Messages */
    .stChatMessage {
        background: white;
        border-radius: 14px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        border: 1px solid #e0e6ed;
    }
    
    /* User Message */
    [data-testid="stChatMessageContainer"] .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #667eea;
    }
    
    /* Assistant Message */
    [data-testid="stChatMessageContainer"] .stChatMessage[data-testid="assistant-message"] {
        background: white;
        border-left: 4px solid #48c774;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        border-radius: 10px;
        border: 2px solid #e0e6ed;
        background: #f8f9fa;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
    }
    
    /* File Uploader */
    .stFileUploader > div {
        border: 2px dashed #667eea;
        border-radius: 12px;
        background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%);
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    .stFileUploader > div:hover {
        border-color: #764ba2;
        background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%);
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        height: 8px;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #e0e6ed;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    /* Info Box */
    .stInfo {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border-left: 4px solid #2196f3;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Success Box */
    .stSuccess {
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-left: 4px solid #4caf50;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Warning Box */
    .stWarning {
        background: linear-gradient(135deg, #fff3e0 0%, #ffe0b2 100%);
        border-left: 4px solid #ff9800;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Error Box */
    .stError {
        background: linear-gradient(135deg, #ffebee 0%, #ffcdd2 100%);
        border-left: 4px solid #f44336;
        border-radius: 8px;
        padding: 1rem;
    }
    
    /* Modern Divider */
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #e0e6ed, transparent);
        margin: 2rem 0;
    }
    
    /* Voice System Card */
    .voice-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        border: 2px solid #667eea;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
        margin: 2rem 0;
    }
    
    /* Audio Recorder Button */
    .stAudioRecorder {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 50%;
        padding: 1.5rem;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stAudioRecorder:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 32px rgba(102, 126, 234, 0.4);
    }
    
    /* Tab Styling */
    .stTabs > div > div > div > button {
        background: transparent;
        border-bottom: 2px solid transparent;
        font-weight: 600;
        color: #666;
        transition: all 0.3s ease;
    }
    
    .stTabs > div > div > div > button[aria-selected="true"] {
        border-bottom-color: #667eea;
        color: #667eea;
    }
    
    /* Modern Checkbox */
    .stCheckbox > label > div {
        border-radius: 6px;
        border: 2px solid #e0e6ed;
        transition: all 0.3s ease;
    }
    
    .stCheckbox > label > div[data-checked="true"] {
        background: #667eea;
        border-color: #667eea;
    }
    
    /* Container Styling */
    .main-container {
        max-width: 1400px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #1e3c72;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Modern Table */
    .dataframe {
        border: none !important;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }
    
    .dataframe thead tr {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .dataframe tbody tr:hover {
        background: #f8f9fa;
    }
    
    /* Loading Animation */
    .stSpinner > div {
        border-color: #667eea;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# HEADER WITH MODERN DESIGN
st.markdown("""
<div class="main-header">
    <h1 class="app-title">Izza MD PhD</h1>
    <p class="app-subtitle">Advanced Medical Intelligence System</p>
</div>
""", unsafe_allow_html=True)

# MEDICAL DISCLAIMER WITH MODERN DESIGN
st.markdown("""
<div class="medical-alert">
    <h4>⚕️ IMPORTANT MEDICAL DISCLAIMER</h4>
    <p>
        This AI system is designed for educational and diagnostic support purposes only.
        It does NOT replace professional medical consultation. Always seek qualified medical advice
        for actual diagnoses and treatments. In emergencies, immediately contact emergency services.
    </p>
</div>
""", unsafe_allow_html=True)