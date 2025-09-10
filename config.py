#!/usr/bin/env python3
"""
NEXUS-MED ULTRA - Configuration Module
Central configuration for the medical intelligence system
"""

import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
for directory in [DATA_DIR, LOGS_DIR, REPORTS_DIR, TEMP_DIR]:
    directory.mkdir(exist_ok=True)

# Database configuration
DATABASE_PATH = DATA_DIR / "medical_database.db"
BACKUP_DATABASE_PATH = DATA_DIR / "medical_database_backup.db"

# API Configuration
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
ANTHROPIC_MODEL = "claude-3-opus-20240229"
MAX_TOKENS = 4000
TEMPERATURE = 0.3

# Medical Knowledge Base Configuration
MEDICAL_SPECIALTIES = [
    "Cardiology", "Neurology", "Oncology", "Pediatrics", "Psychiatry",
    "Radiology", "Surgery", "Internal Medicine", "Emergency Medicine",
    "Dermatology", "Ophthalmology", "Orthopedics", "Gynecology",
    "Urology", "Endocrinology", "Gastroenterology", "Pulmonology",
    "Nephrology", "Rheumatology", "Infectious Disease"
]

# Risk thresholds
RISK_THRESHOLDS = {
    'early_warning_score': {
        'minimal': 0,
        'low': 1,
        'medium': 3,
        'high': 5,
        'critical': 7
    },
    'readmission_probability': {
        'low': 0.3,
        'medium': 0.5,
        'high': 0.7
    }
}

# Vital signs normal ranges
VITAL_SIGNS_RANGES = {
    'heart_rate': {'min': 60, 'max': 100, 'unit': 'bpm'},
    'bp_systolic': {'min': 90, 'max': 140, 'unit': 'mmHg'},
    'bp_diastolic': {'min': 60, 'max': 90, 'unit': 'mmHg'},
    'temperature': {'min': 36.5, 'max': 37.5, 'unit': '°C'},
    'respiratory_rate': {'min': 12, 'max': 20, 'unit': 'breaths/min'},
    'spo2': {'min': 95, 'max': 100, 'unit': '%'}
}

# Lab test categories
LAB_TEST_CATEGORIES = [
    "Hematology", "Chemistry", "Immunology", "Microbiology",
    "Molecular", "Urinalysis", "Coagulation", "Blood Gases",
    "Endocrinology", "Toxicology"
]

# Report settings
REPORT_SETTINGS = {
    'page_size': 'A4',
    'margin': 72,  # 1 inch
    'font_family': 'Helvetica',
    'title_font_size': 24,
    'subtitle_font_size': 18,
    'body_font_size': 12,
    'footer_font_size': 10
}

# UI Theme
UI_THEME = {
    'primary_color': '#FF0000',
    'secondary_color': '#8B0000',
    'accent_color': '#DC143C',
    'background_color': '#FFFFFF',
    'text_color': '#333333',
    'success_color': '#28A745',
    'warning_color': '#FFC107',
    'danger_color': '#DC3545',
    'info_color': '#17A2B8'
}

# Feature flags
FEATURES = {
    'enable_ml_predictions': True,
    'enable_drug_interactions': True,
    'enable_telemedicine': True,
    'enable_research_assistant': True,
    'enable_voice_input': False,
    'enable_multi_language': False,
    'enable_cloud_sync': False,
    'enable_notifications': True,
    'enable_analytics': True,
    'enable_export': True
}

# System messages
SYSTEM_MESSAGES = {
    'welcome': "Welcome to NEXUS-MED ULTRA v5.0 - Advanced Medical Intelligence System",
    'emergency_warning': "🚨 EMERGENCY DETECTED - Immediate medical attention required!",
    'high_risk_alert': "⚠️ HIGH RISK - Close monitoring recommended",
    'data_saved': "✅ Data saved successfully",
    'error_generic': "❌ An error occurred. Please try again.",
    'loading': "⏳ Processing your request...",
    'no_patient': "⚡ Please select or create a patient profile first"
}

# Export settings
EXPORT_FORMATS = ['PDF', 'Excel', 'CSV', 'JSON', 'DOCX']
MAX_EXPORT_SIZE_MB = 50

# Session settings
SESSION_TIMEOUT_MINUTES = 30
MAX_CONVERSATION_LENGTH = 100
AUTO_SAVE_INTERVAL_SECONDS = 300

# Logging configuration
LOG_LEVEL = 'INFO'
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
MAX_LOG_SIZE_MB = 10
LOG_BACKUP_COUNT = 5

# Security settings
ENABLE_ENCRYPTION = True
MIN_PASSWORD_LENGTH = 8
SESSION_TOKEN_LENGTH = 32
MAX_LOGIN_ATTEMPTS = 5

# Performance settings
CACHE_SIZE_MB = 100
MAX_CONCURRENT_REQUESTS = 10
REQUEST_TIMEOUT_SECONDS = 300
DATABASE_POOL_SIZE = 5

# Integration endpoints
PUBMED_API_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
CLINICAL_TRIALS_API_URL = "https://clinicaltrials.gov/api/query/"
DRUG_INTERACTION_API_URL = "https://rxnav.nlm.nih.gov/REST/"

# Email settings (for notifications)
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@nexusmed.com')

# Backup settings
ENABLE_AUTO_BACKUP = True
BACKUP_INTERVAL_HOURS = 24
MAX_BACKUPS_TO_KEEP = 7
BACKUP_COMPRESSION = True

# Analytics settings
ANALYTICS_RETENTION_DAYS = 365
ENABLE_ANONYMOUS_ANALYTICS = False
ANALYTICS_SAMPLE_RATE = 1.0

# Telemedicine settings
VIDEO_QUALITY = 'high'  # low, medium, high
AUDIO_QUALITY = 'high'
MAX_CALL_DURATION_MINUTES = 60
ENABLE_RECORDING = False
ENABLE_SCREEN_SHARE = True

# Research settings
MAX_RESEARCH_RESULTS = 50
ENABLE_FULL_TEXT_SEARCH = True
RESEARCH_CACHE_HOURS = 24

# Notification settings
NOTIFICATION_CHANNELS = ['in_app', 'email', 'sms']
CRITICAL_ALERT_DELAY_SECONDS = 0
HIGH_ALERT_DELAY_SECONDS = 300
MEDIUM_ALERT_DELAY_SECONDS = 3600

# Development settings
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
TESTING = os.getenv('TESTING', 'False').lower() == 'true'
PROFILING = os.getenv('PROFILING', 'False').lower() == 'true'

# Validate critical settings
def validate_config():
    """Validate critical configuration settings"""
    errors = []
    
    if not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY not set in environment variables")
    
    if not DATABASE_PATH.parent.exists():
        errors.append(f"Database directory does not exist: {DATABASE_PATH.parent}")
    
    if MAX_TOKENS < 1000:
        errors.append("MAX_TOKENS should be at least 1000")
    
    if TEMPERATURE < 0 or TEMPERATURE > 1:
        errors.append("TEMPERATURE should be between 0 and 1")
    
    return errors

# Load custom configuration if exists
CUSTOM_CONFIG_PATH = BASE_DIR / "custom_config.py"
if CUSTOM_CONFIG_PATH.exists():
    import importlib.util
    spec = importlib.util.spec_from_file_location("custom_config", CUSTOM_CONFIG_PATH)
    custom_config = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(custom_config)
    
    # Override default settings with custom ones
    for attr in dir(custom_config):
        if not attr.startswith('_'):
            globals()[attr] = getattr(custom_config, attr)

if __name__ == "__main__":
    # Test configuration
    print("NEXUS-MED ULTRA Configuration Test")
    print("=" * 50)
    print(f"Base Directory: {BASE_DIR}")
    print(f"Database Path: {DATABASE_PATH}")
    print(f"API Key Set: {'Yes' if ANTHROPIC_API_KEY else 'No'}")
    print(f"Debug Mode: {DEBUG}")
    print(f"Features Enabled: {sum(FEATURES.values())}/{len(FEATURES)}")
    
    errors = validate_config()
    if errors:
        print("\nConfiguration Errors:")
        for error in errors:
            print(f"❌ {error}")
    else:
        print("\n✅ Configuration valid!")
