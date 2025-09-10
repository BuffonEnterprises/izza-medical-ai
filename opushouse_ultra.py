import streamlit as st
from anthropic import Anthropic
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv
import httpx
import json
from typing import Optional, List, Dict, Any, Tuple, Union
import re
import time
import base64
from PIL import Image
import PyPDF2
import io
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hashlib
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
import sqlite3
from concurrent.futures import ThreadPoolExecutor
import asyncio
try:
    import aiohttp
except ImportError:
    aiohttp = None
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    TfidfVectorizer = None
    cosine_similarity = None
try:
    import nltk
except ImportError:
    nltk = None
from collections import Counter, defaultdict
import random
import string
import zipfile
import tempfile
import shutil
import subprocess
import platform
try:
    import psutil
except ImportError:
    psutil = None
import socket
try:
    import qrcode
except ImportError:
    qrcode = None
from io import BytesIO
import xml.etree.ElementTree as ET
try:
    import yaml
except ImportError:
    yaml = None
try:
    import toml
except ImportError:
    toml = None
import csv
try:
    import xlsxwriter
except ImportError:
    xlsxwriter = None
try:
    from openpyxl import load_workbook
except ImportError:
    load_workbook = None
try:
    import docx
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
except ImportError:
    docx = None
try:
    import fitz  # PyMuPDF
except ImportError:
    fitz = None
try:
    import pdfplumber
except ImportError:
    pdfplumber = None
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from reportlab.platypus.flowables import HRFlowable
try:
    from reportlab.graphics.shapes import Drawing
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.graphics.charts.linecharts import HorizontalLineChart
except ImportError:
    Drawing = None
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
try:
    import schedule
except ImportError:
    schedule = None
import threading
import logging
from logging.handlers import RotatingFileHandler
import warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('medical_app.log', maxBytes=10485760, backupCount=5),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Advanced Medical Database Schema
@dataclass
class Patient:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    name: str = ""
    age: int = 0
    gender: str = ""
    blood_type: str = ""
    height: float = 0.0
    weight: float = 0.0
    bmi: float = 0.0
    allergies: List[str] = field(default_factory=list)
    chronic_conditions: List[str] = field(default_factory=list)
    current_medications: List[Dict[str, Any]] = field(default_factory=list)
    medical_history: List[Dict[str, Any]] = field(default_factory=list)
    family_history: List[Dict[str, Any]] = field(default_factory=list)
    surgical_history: List[Dict[str, Any]] = field(default_factory=list)
    immunization_records: List[Dict[str, Any]] = field(default_factory=list)
    emergency_contact: Dict[str, str] = field(default_factory=dict)
    insurance_info: Dict[str, str] = field(default_factory=dict)
    social_history: Dict[str, Any] = field(default_factory=dict)
    genetic_data: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    last_visit: str = ""
    next_appointment: str = ""
    risk_factors: List[str] = field(default_factory=list)
    
    def calculate_bmi(self):
        if self.height > 0 and self.weight > 0:
            self.bmi = self.weight / ((self.height / 100) ** 2)
        return self.bmi

@dataclass
class MedicalRecord:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    visit_date: str = field(default_factory=lambda: datetime.now().isoformat())
    visit_type: str = ""  # Emergency, Routine, Follow-up, Telemedicine
    chief_complaint: str = ""
    history_of_present_illness: str = ""
    symptoms: List[str] = field(default_factory=list)
    symptom_duration: Dict[str, str] = field(default_factory=dict)
    symptom_severity: Dict[str, int] = field(default_factory=dict)
    vital_signs: Dict[str, float] = field(default_factory=dict)
    physical_examination: Dict[str, str] = field(default_factory=dict)
    diagnosis: List[str] = field(default_factory=list)
    differential_diagnosis: List[str] = field(default_factory=list)
    icd_codes: List[str] = field(default_factory=list)
    treatment_plan: str = ""
    prescriptions: List[Dict[str, Any]] = field(default_factory=list)
    procedures_performed: List[str] = field(default_factory=list)
    lab_orders: List[Dict[str, Any]] = field(default_factory=list)
    lab_results: List[Dict[str, Any]] = field(default_factory=list)
    imaging_orders: List[Dict[str, Any]] = field(default_factory=list)
    imaging_results: List[Dict[str, Any]] = field(default_factory=list)
    referrals: List[Dict[str, str]] = field(default_factory=list)
    notes: str = ""
    follow_up: str = ""
    prognosis: str = ""
    provider: str = ""
    billing_codes: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    modified_at: str = field(default_factory=lambda: datetime.now().isoformat())

@dataclass
class Prescription:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    patient_id: str = ""
    record_id: str = ""
    medication_name: str = ""
    generic_name: str = ""
    dosage: str = ""
    frequency: str = ""
    route: str = ""
    duration: str = ""
    quantity: int = 0
    refills: int = 0
    instructions: str = ""
    indication: str = ""
    prescriber: str = ""
    pharmacy: str = ""
    date_prescribed: str = field(default_factory=lambda: datetime.now().isoformat())
    date_filled: str = ""
    date_expired: str = ""
    status: str = "Active"  # Active, Discontinued, Completed
    contraindications_checked: bool = False
    interactions_checked: bool = False
    allergies_checked: bool = False

class MedicalSpecialty(Enum):
    CARDIOLOGY = "Cardiology"
    NEUROLOGY = "Neurology"
    ONCOLOGY = "Oncology"
    PEDIATRICS = "Pediatrics"
    PSYCHIATRY = "Psychiatry"
    RADIOLOGY = "Radiology"
    SURGERY = "Surgery"
    INTERNAL_MEDICINE = "Internal Medicine"
    EMERGENCY_MEDICINE = "Emergency Medicine"
    DERMATOLOGY = "Dermatology"
    OPHTHALMOLOGY = "Ophthalmology"
    ORTHOPEDICS = "Orthopedics"
    GYNECOLOGY = "Gynecology"
    UROLOGY = "Urology"
    ENDOCRINOLOGY = "Endocrinology"
    GASTROENTEROLOGY = "Gastroenterology"
    PULMONOLOGY = "Pulmonology"
    RHEUMATOLOGY = "Rheumatology"
    NEPHROLOGY = "Nephrology"
    HEMATOLOGY = "Hematology"
    INFECTIOUS_DISEASE = "Infectious Disease"
    ANESTHESIOLOGY = "Anesthesiology"
    PATHOLOGY = "Pathology"
    PHYSICAL_MEDICINE = "Physical Medicine & Rehabilitation"

class SymptomSeverity(Enum):
    MILD = 1
    MODERATE = 2
    SEVERE = 3
    CRITICAL = 4
    LIFE_THREATENING = 5

class LabTestStatus(Enum):
    ORDERED = "Ordered"
    PENDING = "Pending"
    IN_PROGRESS = "In Progress"
    COMPLETED = "Completed"
    CANCELLED = "Cancelled"
    ABNORMAL = "Abnormal"
    CRITICAL = "Critical"

# Enhanced Medical Knowledge Database
class MedicalKnowledgeBase:
    def __init__(self):
        self.symptoms_database = self._init_symptoms_database()
        self.drug_database = self._init_drug_database()
        self.lab_reference_ranges = self._init_lab_references()
        self.clinical_guidelines = self._init_clinical_guidelines()
        self.medical_calculators = self._init_medical_calculators()
        self.diagnostic_criteria = self._init_diagnostic_criteria()
        self.treatment_protocols = self._init_treatment_protocols()
        self.emergency_protocols = self._init_emergency_protocols()
        self.medical_abbreviations = self._init_medical_abbreviations()
        self.anatomy_database = self._init_anatomy_database()
        
    def _init_symptoms_database(self):
        return {
            "chest_pain": {
                "possible_conditions": [
                    "Myocardial Infarction", "Unstable Angina", "Stable Angina",
                    "Pulmonary Embolism", "Aortic Dissection", "Pneumothorax",
                    "Pericarditis", "Myocarditis", "Costochondritis", "GERD",
                    "Panic Attack", "Pleurisy", "Pneumonia", "Rib Fracture"
                ],
                "red_flags": [
                    "Radiating to arm/jaw/back", "Shortness of breath", "Diaphoresis",
                    "Nausea/vomiting", "Sudden onset", "Crushing/pressure sensation",
                    "Hypotension", "Altered mental status", "Cyanosis"
                ],
                "emergency": True,
                "specialty": MedicalSpecialty.CARDIOLOGY,
                "initial_workup": ["ECG", "Troponin", "Chest X-ray", "D-dimer", "CTA chest"],
                "physical_exam": ["Vital signs", "Cardiac auscultation", "Lung auscultation", "JVD assessment"],
                "history_points": ["Duration", "Quality", "Radiation", "Associated symptoms", "Triggers", "Relieving factors"]
            },
            "headache": {
                "possible_conditions": [
                    "Migraine", "Tension Headache", "Cluster Headache",
                    "Subarachnoid Hemorrhage", "Meningitis", "Encephalitis",
                    "Brain Tumor", "Temporal Arteritis", "Sinusitis",
                    "Intracranial Hypertension", "Medication Overuse", "Trigeminal Neuralgia"
                ],
                "red_flags": [
                    "Thunderclap onset", "Fever with neck stiffness", "Focal neurological deficits",
                    "Papilledema", "New onset >50 years", "Immunocompromised state",
                    "Worse with Valsalva", "Progressive pattern", "Personality changes"
                ],
                "emergency": False,
                "specialty": MedicalSpecialty.NEUROLOGY,
                "initial_workup": ["Neurological exam", "CT head", "LP if indicated", "ESR/CRP", "MRI brain"],
                "physical_exam": ["Fundoscopy", "Cranial nerves", "Motor/sensory exam", "Reflexes", "Meningeal signs"],
                "history_points": ["Pattern", "Triggers", "Aura", "Family history", "Medications", "Vision changes"]
            },
            "abdominal_pain": {
                "possible_conditions": [
                    "Appendicitis", "Cholecystitis", "Pancreatitis", "Peptic Ulcer",
                    "Bowel Obstruction", "Diverticulitis", "Kidney Stones", "UTI",
                    "Ectopic Pregnancy", "Ovarian Torsion", "AAA", "Mesenteric Ischemia",
                    "Inflammatory Bowel Disease", "Gastroenteritis", "Hepatitis"
                ],
                "red_flags": [
                    "Peritoneal signs", "Hemodynamic instability", "Severe constant pain",
                    "Fever >38.5°C", "Hematemesis/melena", "Positive pregnancy test",
                    "Pulsatile mass", "Acute onset", "Immunocompromised"
                ],
                "emergency": True,
                "specialty": MedicalSpecialty.SURGERY,
                "initial_workup": ["CBC", "BMP", "LFTs", "Lipase", "Urinalysis", "βhCG", "CT abdomen/pelvis"],
                "physical_exam": ["Abdominal inspection", "Palpation", "Percussion", "Auscultation", "Rectal exam"],
                "history_points": ["Location", "Onset", "Character", "Radiation", "Timing", "Associated symptoms"]
            },
            "shortness_of_breath": {
                "possible_conditions": [
                    "Pulmonary Embolism", "Pneumonia", "COPD Exacerbation", "Asthma",
                    "CHF Exacerbation", "Pneumothorax", "ARDS", "Pulmonary Edema",
                    "Anemia", "Anxiety", "Pleural Effusion", "Pulmonary Fibrosis"
                ],
                "red_flags": [
                    "Sudden onset", "Chest pain", "Hemoptysis", "Hypoxia",
                    "Tachycardia", "Hypotension", "Altered mental status",
                    "Unilateral leg swelling", "Recent surgery/immobility"
                ],
                "emergency": True,
                "specialty": MedicalSpecialty.PULMONOLOGY,
                "initial_workup": ["ABG", "Chest X-ray", "D-dimer", "BNP", "ECG", "CTA chest if PE suspected"],
                "physical_exam": ["Respiratory rate", "O2 saturation", "Lung auscultation", "Heart sounds", "Extremity exam"],
                "history_points": ["Onset", "Progression", "Orthopnea", "PND", "Exercise tolerance", "Exposures"]
            },
            "fever": {
                "possible_conditions": [
                    "Sepsis", "UTI", "Pneumonia", "Meningitis", "Endocarditis",
                    "Abscess", "Cellulitis", "Viral Infection", "Drug Fever",
                    "Malignancy", "Autoimmune Disease", "Thyroid Storm"
                ],
                "red_flags": [
                    "Hypotension", "Altered mental status", "Petechiae", "Neck stiffness",
                    "New murmur", "Immunocompromised", "Recent travel", "IV drug use"
                ],
                "emergency": False,
                "specialty": MedicalSpecialty.INFECTIOUS_DISEASE,
                "initial_workup": ["CBC with diff", "Blood cultures", "UA with culture", "CXR", "Lactate"],
                "physical_exam": ["Complete vital signs", "Skin exam", "Lymph nodes", "Heart/lung exam", "Abdominal exam"],
                "history_points": ["Duration", "Pattern", "Associated symptoms", "Exposures", "Travel", "Medications"]
            }
        }
    
    def _init_drug_database(self):
        return {
            "metformin": {
                "class": "Biguanide",
                "mechanism": "Decreases hepatic glucose production, increases insulin sensitivity",
                "indications": ["Type 2 Diabetes", "PCOS", "Prediabetes"],
                "contraindications": ["eGFR <30", "Acute kidney injury", "Metabolic acidosis", "Severe hepatic disease"],
                "interactions": ["Contrast dye", "Alcohol", "Carbonic anhydrase inhibitors"],
                "dosage": {
                    "adult": "Start 500mg BID, max 2000mg/day",
                    "pediatric": "10-16 years: 500mg BID, max 2000mg/day",
                    "renal_adjustment": "eGFR 30-45: reduce dose by 50%"
                },
                "side_effects": ["GI upset", "B12 deficiency", "Lactic acidosis (rare)"],
                "monitoring": ["Renal function", "B12 levels annually", "HbA1c q3-6 months"],
                "counseling": ["Take with meals", "Avoid excessive alcohol", "Stop before contrast procedures"]
            },
            "lisinopril": {
                "class": "ACE Inhibitor",
                "mechanism": "Inhibits ACE, reducing angiotensin II formation",
                "indications": ["Hypertension", "Heart failure", "Post-MI", "Diabetic nephropathy"],
                "contraindications": ["Pregnancy", "Bilateral renal artery stenosis", "Angioedema history", "Hyperkalemia"],
                "interactions": ["NSAIDs", "Potassium supplements", "Lithium", "Aliskiren"],
                "dosage": {
                    "adult": "HTN: 10mg daily, max 40mg; HF: 5mg daily, max 40mg",
                    "pediatric": "≥6 years: 0.07mg/kg daily, max 5mg",
                    "renal_adjustment": "CrCl <30: reduce initial dose by 50%"
                },
                "side_effects": ["Dry cough", "Hyperkalemia", "Angioedema", "Hypotension", "AKI"],
                "monitoring": ["BP", "Potassium", "Creatinine", "Monitor for cough"],
                "counseling": ["May cause dizziness", "Report swelling of face/tongue", "Avoid salt substitutes"]
            },
            "atorvastatin": {
                "class": "HMG-CoA Reductase Inhibitor (Statin)",
                "mechanism": "Inhibits HMG-CoA reductase, reducing cholesterol synthesis",
                "indications": ["Hyperlipidemia", "ASCVD prevention", "Post-MI", "Diabetes with risk factors"],
                "contraindications": ["Active liver disease", "Pregnancy", "Breastfeeding"],
                "interactions": ["CYP3A4 inhibitors", "Fibrates", "Niacin", "Cyclosporine"],
                "dosage": {
                    "adult": "10-80mg daily, high intensity: 40-80mg",
                    "pediatric": "10-17 years: 10-20mg daily",
                    "hepatic_adjustment": "Use with caution, avoid in active disease"
                },
                "side_effects": ["Myalgia", "Elevated LFTs", "Rhabdomyolysis (rare)", "New-onset diabetes"],
                "monitoring": ["Lipid panel", "LFTs", "CPK if symptoms", "HbA1c in diabetics"],
                "counseling": ["Take in evening", "Report muscle pain", "Avoid grapefruit juice"]
            }
        }
    
    def _init_lab_references(self):
        return {
            "CBC": {
                "WBC": {"min": 4.5, "max": 11.0, "unit": "10^9/L", "critical_low": 2.0, "critical_high": 30.0},
                "RBC": {
                    "male": {"min": 4.5, "max": 5.5, "unit": "10^12/L"},
                    "female": {"min": 4.0, "max": 5.0, "unit": "10^12/L"}
                },
                "Hemoglobin": {
                    "male": {"min": 13.5, "max": 17.5, "unit": "g/dL", "critical_low": 7.0, "critical_high": 20.0},
                    "female": {"min": 12.0, "max": 15.5, "unit": "g/dL", "critical_low": 7.0, "critical_high": 20.0}
                },
                "Hematocrit": {
                    "male": {"min": 40, "max": 54, "unit": "%"},
                    "female": {"min": 36, "max": 46, "unit": "%"}
                },
                "Platelets": {"min": 150, "max": 400, "unit": "10^9/L", "critical_low": 20, "critical_high": 1000},
                "MCV": {"min": 80, "max": 100, "unit": "fL"},
                "MCH": {"min": 27, "max": 31, "unit": "pg"},
                "MCHC": {"min": 32, "max": 36, "unit": "g/dL"},
                "RDW": {"min": 11.5, "max": 14.5, "unit": "%"}
            },
            "CMP": {
                "Glucose": {"min": 70, "max": 100, "unit": "mg/dL", "critical_low": 40, "critical_high": 500},
                "BUN": {"min": 7, "max": 20, "unit": "mg/dL"},
                "Creatinine": {
                    "male": {"min": 0.7, "max": 1.3, "unit": "mg/dL"},
                    "female": {"min": 0.6, "max": 1.1, "unit": "mg/dL"}
                },
                "eGFR": {"min": 90, "max": 120, "unit": "mL/min/1.73m²"},
                "Sodium": {"min": 136, "max": 145, "unit": "mEq/L", "critical_low": 120, "critical_high": 160},
                "Potassium": {"min": 3.5, "max": 5.1, "unit": "mEq/L", "critical_low": 2.5, "critical_high": 6.5},
                "Chloride": {"min": 98, "max": 107, "unit": "mEq/L"},
                "CO2": {"min": 22, "max": 29, "unit": "mEq/L"},
                "Calcium": {"min": 8.5, "max": 10.5, "unit": "mg/dL", "critical_low": 6.0, "critical_high": 13.0},
                "Total_Protein": {"min": 6.3, "max": 8.2, "unit": "g/dL"},
                "Albumin": {"min": 3.5, "max": 5.0, "unit": "g/dL"},
                "Bilirubin_Total": {"min": 0.2, "max": 1.2, "unit": "mg/dL"},
                "ALP": {"min": 44, "max": 147, "unit": "IU/L"},
                "AST": {"min": 10, "max": 40, "unit": "IU/L"},
                "ALT": {"min": 7, "max": 56, "unit": "IU/L"}
            },
            "Lipid_Panel": {
                "Total_Cholesterol": {"optimal": "<200", "borderline": "200-239", "high": "≥240", "unit": "mg/dL"},
                "LDL": {"optimal": "<100", "near_optimal": "100-129", "borderline": "130-159", "high": "160-189", "very_high": "≥190", "unit": "mg/dL"},
                "HDL": {
                    "male": {"low": "<40", "normal": "≥40", "unit": "mg/dL"},
                    "female": {"low": "<50", "normal": "≥50", "unit": "mg/dL"}
                },
                "Triglycerides": {"normal": "<150", "borderline": "150-199", "high": "200-499", "very_high": "≥500", "unit": "mg/dL"}
            },
            "Thyroid": {
                "TSH": {"min": 0.4, "max": 4.5, "unit": "mIU/L"},
                "Free_T4": {"min": 0.8, "max": 1.8, "unit": "ng/dL"},
                "Free_T3": {"min": 2.3, "max": 4.2, "unit": "pg/mL"}
            },
            "Cardiac": {
                "Troponin_I": {"normal": "<0.04", "unit": "ng/mL", "MI_cutoff": ">0.04"},
                "BNP": {"normal": "<100", "unit": "pg/mL", "HF_likely": ">400"},
                "Pro_BNP": {"normal": "<300", "unit": "pg/mL", "age_adjusted": True},
                "CK_MB": {"min": 0, "max": 6.3, "unit": "ng/mL"},
                "Myoglobin": {"min": 25, "max": 72, "unit": "ng/mL"}
            }
        }
    
    def _init_clinical_guidelines(self):
        return {
            "hypertension": {
                "definition": "Sustained elevation of BP ≥130/80 mmHg",
                "stages": {
                    "normal": {"systolic": "<120", "diastolic": "<80"},
                    "elevated": {"systolic": "120-129", "diastolic": "<80"},
                    "stage_1": {"systolic": "130-139", "diastolic": "80-89"},
                    "stage_2": {"systolic": "≥140", "diastolic": "≥90"},
                    "crisis": {"systolic": ">180", "diastolic": ">120"}
                },
                "workup": ["CBC", "BMP", "Lipids", "TSH", "Urinalysis", "ECG", "Echo if indicated"],
                "first_line": ["ACE/ARB", "CCB", "Thiazide"],
                "compelling_indications": {
                    "Heart_failure": ["ACE/ARB", "BB", "Aldosterone antagonist"],
                    "Post_MI": ["BB", "ACE/ARB"],
                    "CKD": ["ACE/ARB"],
                    "Diabetes": ["ACE/ARB"]
                },
                "lifestyle": ["DASH diet", "Weight loss", "Exercise 150min/week", "Sodium <2.3g/day", "Limit alcohol"],
                "followup": "Stage 1: 3-6 months, Stage 2: 1 month"
            },
            "diabetes": {
                "diagnosis": {
                    "FPG": "≥126 mg/dL on two occasions",
                    "OGTT": "≥200 mg/dL at 2 hours",
                    "HbA1c": "≥6.5%",
                    "Random": "≥200 mg/dL with symptoms"
                },
                "targets": {
                    "HbA1c": "<7% for most, <8% if elderly/comorbid",
                    "FPG": "80-130 mg/dL",
                    "PPG": "<180 mg/dL",
                    "BP": "<140/90, <130/80 if high risk",
                    "LDL": "<100, <70 if ASCVD"
                },
                "screening": {
                    "Age": "≥45 years or earlier if risk factors",
                    "Frequency": "Every 3 years if normal, annually if prediabetes"
                },
                "medications": {
                    "First_line": "Metformin",
                    "Second_line": ["GLP-1 RA", "SGLT-2i", "DPP-4i", "Sulfonylurea"],
                    "Injectable": ["GLP-1 RA", "Insulin"]
                },
                "complications_screening": {
                    "Retinopathy": "Annual dilated eye exam",
                    "Nephropathy": "Annual urine albumin, eGFR",
                    "Neuropathy": "Annual foot exam",
                    "ASCVD": "Lipids annually, consider ASA"
                }
            },
            "asthma": {
                "classification": {
                    "Intermittent": "Symptoms ≤2 days/week, nighttime ≤2x/month",
                    "Mild_persistent": "Symptoms >2 days/week, nighttime 3-4x/month",
                    "Moderate_persistent": "Daily symptoms, nighttime >1x/week",
                    "Severe_persistent": "Throughout day, nighttime often"
                },
                "stepwise_treatment": {
                    "Step_1": "PRN SABA",
                    "Step_2": "Low-dose ICS",
                    "Step_3": "Low-dose ICS/LABA or medium-dose ICS",
                    "Step_4": "Medium-dose ICS/LABA",
                    "Step_5": "High-dose ICS/LABA + consider add-on",
                    "Step_6": "High-dose ICS/LABA + oral steroids"
                },
                "exacerbation": {
                    "Mild": "SABA q20min x3, oral steroids",
                    "Moderate": "SABA + ipratropium, steroids, O2 to >90%",
                    "Severe": "Continuous nebs, IV steroids, consider Mg, admission"
                },
                "monitoring": ["Peak flow", "Symptom diary", "Spirometry yearly", "ACT score"]
            }
        }
    
    def _init_medical_calculators(self):
        return {
            "CHADS2_VASc": {
                "description": "Stroke risk in AFib",
                "components": {
                    "CHF": 1,
                    "Hypertension": 1,
                    "Age_75+": 2,
                    "Diabetes": 1,
                    "Stroke/TIA": 2,
                    "Vascular_disease": 1,
                    "Age_65-74": 1,
                    "Female": 1
                },
                "interpretation": {
                    0: "Low risk - Consider no therapy or ASA",
                    1: "Low-moderate - Consider anticoagulation",
                    "≥2": "Moderate-high - Anticoagulation recommended"
                }
            },
            "CURB65": {
                "description": "Pneumonia severity",
                "components": {
                    "Confusion": 1,
                    "Urea_>7mmol/L": 1,
                    "RR_≥30": 1,
                    "BP_<90/60": 1,
                    "Age_≥65": 1
                },
                "interpretation": {
                    "0-1": "Low risk - Consider outpatient",
                    "2": "Moderate - Consider admission",
                    "≥3": "High risk - Admit, consider ICU"
                }
            },
            "Wells_PE": {
                "description": "PE probability",
                "components": {
                    "Clinical_signs_DVT": 3,
                    "PE_likely": 3,
                    "HR_>100": 1.5,
                    "Immobilization/surgery": 1.5,
                    "Previous_PE/DVT": 1.5,
                    "Hemoptysis": 1,
                    "Malignancy": 1
                },
                "interpretation": {
                    "<2": "Low probability - Consider D-dimer",
                    "2-6": "Moderate probability - Consider CTA",
                    ">6": "High probability - Consider CTA or treat empirically"
                }
            },
            "MELD": {
                "description": "Liver disease severity",
                "formula": "10 × (0.957 × ln(Cr) + 0.378 × ln(bili) + 1.12 × ln(INR)) + 6.43",
                "interpretation": {
                    "<10": "1.9% 3-month mortality",
                    "10-19": "6-20% 3-month mortality",
                    "20-29": "20-50% 3-month mortality",
                    "≥30": ">50% 3-month mortality"
                }
            }
        }
    
    def _init_diagnostic_criteria(self):
        return {
            "SIRS": {
                "criteria": [
                    "Temperature >38°C or <36°C",
                    "Heart rate >90",
                    "Respiratory rate >20 or PaCO2 <32",
                    "WBC >12,000 or <4,000 or >10% bands"
                ],
                "diagnosis": "≥2 criteria"
            },
            "Sepsis": {
                "definition": "Life-threatening organ dysfunction due to dysregulated host response to infection",
                "criteria": "Infection + organ dysfunction (SOFA ≥2)",
                "qSOFA": ["RR ≥22", "Altered mentation", "SBP ≤100"],
                "diagnosis": "≥2 qSOFA criteria suggests sepsis"
            },
            "Metabolic_Syndrome": {
                "criteria": [
                    "Waist circumference: M >40in, F >35in",
                    "Triglycerides ≥150 mg/dL",
                    "HDL: M <40, F <50 mg/dL",
                    "BP ≥130/85",
                    "Fasting glucose ≥100 mg/dL"
                ],
                "diagnosis": "≥3 criteria"
            },
            "Rheumatoid_Arthritis": {
                "ACR_EULAR_2010": {
                    "Joint_involvement": {
                        "1 large": 0,
                        "2-10 large": 1,
                        "1-3 small": 2,
                        "4-10 small": 3,
                        ">10 (at least 1 small)": 5
                    },
                    "Serology": {
                        "RF and ACPA negative": 0,
                        "Low positive RF or ACPA": 2,
                        "High positive RF or ACPA": 3
                    },
                    "Acute_phase": {
                        "Normal CRP and ESR": 0,
                        "Abnormal CRP or ESR": 1
                    },
                    "Duration": {
                        "<6 weeks": 0,
                        "≥6 weeks": 1
                    }
                },
                "diagnosis": "Score ≥6/10"
            }
        }
    
    def _init_treatment_protocols(self):
        return {
            "ACS": {
                "STEMI": {
                    "immediate": ["ASA 325mg", "P2Y12 inhibitor", "Anticoagulation", "Beta-blocker", "Statin"],
                    "reperfusion": "PCI within 90min or fibrinolysis within 30min if PCI not available",
                    "post_MI": ["Dual antiplatelet", "Beta-blocker", "ACE/ARB", "Statin", "Aldosterone antagonist if EF<40%"]
                },
                "NSTEMI": {
                    "medical": ["ASA", "P2Y12 inhibitor", "Anticoagulation", "Beta-blocker", "Statin", "Nitrates PRN"],
                    "invasive": "High risk: <24h, Intermediate: <72h",
                    "risk_stratify": "TIMI or GRACE score"
                }
            },
            "Stroke": {
                "Ischemic": {
                    "hyperacute": "tPA if <4.5h and eligible, thrombectomy if <6-24h for large vessel",
                    "acute": ["ASA 325mg within 48h", "Statin", "DVT prophylaxis", "Swallow eval"],
                    "secondary_prevention": ["Antiplatelet", "Statin", "BP control", "Anticoagulation if AFib"]
                },
                "Hemorrhagic": {
                    "immediate": ["BP control", "Reverse anticoagulation", "Neurosurgery consult"],
                    "ICH_management": ["SBP <140", "ICP monitoring if indicated", "Seizure prophylaxis controversial"]
                }
            },
            "DKA": {
                "initial": {
                    "fluids": "NS 15-20mL/kg/hr x 1hr, then 250-500mL/hr",
                    "insulin": "0.1 units/kg bolus, then 0.1 units/kg/hr infusion",
                    "potassium": "If K <3.3: hold insulin, give K; If 3.3-5.3: give 20-30mEq/L fluids"
                },
                "monitoring": ["Glucose q1h", "BMP q2-4h", "Anion gap q2-4h", "Ketones q2-4h"],
                "transition": "When glucose <200, add dextrose; when gap closed, transition to SubQ insulin"
            }
        }
    
    def _init_emergency_protocols(self):
        return {
            "ACLS": {
                "Cardiac_Arrest": {
                    "VF/VT": ["CPR", "Defibrillate", "Epinephrine q3-5min", "Amiodarone/Lidocaine"],
                    "PEA/Asystole": ["CPR", "Epinephrine q3-5min", "Consider H's and T's"]
                },
                "Post_Arrest": ["Targeted temperature management", "Avoid hyperoxia", "Treat underlying cause"]
            },
            "Anaphylaxis": {
                "treatment": [
                    "Epinephrine 0.3-0.5mg IM",
                    "H1 blocker: Diphenhydramine 50mg",
                    "H2 blocker: Famotidine 20mg",
                    "Steroids: Methylprednisolone 125mg",
                    "Bronchodilators if wheezing",
                    "Fluids for hypotension"
                ],
                "disposition": "Observe 4-6 hours minimum, longer if biphasic risk"
            },
            "Status_Epilepticus": {
                "first_line": "Lorazepam 4mg IV or Diazepam 10mg IV",
                "second_line": ["Fosphenytoin 20mg/kg", "Valproate 40mg/kg", "Levetiracetam 60mg/kg"],
                "refractory": "Propofol or midazolam infusion, EEG monitoring"
            }
        }
    
    def _init_medical_abbreviations(self):
        return {
            "Common": {
                "BP": "Blood Pressure",
                "HR": "Heart Rate",
                "RR": "Respiratory Rate",
                "T": "Temperature",
                "O2": "Oxygen",
                "SOB": "Shortness of Breath",
                "CP": "Chest Pain",
                "Abd": "Abdomen/Abdominal",
                "N/V": "Nausea/Vomiting",
                "HA": "Headache"
            },
            "Diagnostic": {
                "CBC": "Complete Blood Count",
                "BMP": "Basic Metabolic Panel",
                "CMP": "Comprehensive Metabolic Panel",
                "LFT": "Liver Function Test",
                "UA": "Urinalysis",
                "CXR": "Chest X-Ray",
                "CT": "Computed Tomography",
                "MRI": "Magnetic Resonance Imaging",
                "ECG/EKG": "Electrocardiogram",
                "Echo": "Echocardiogram"
            },
            "Medications": {
                "ASA": "Aspirin",
                "APAP": "Acetaminophen",
                "NSAID": "Non-Steroidal Anti-Inflammatory Drug",
                "PPI": "Proton Pump Inhibitor",
                "ACE": "Angiotensin Converting Enzyme",
                "ARB": "Angiotensin Receptor Blocker",
                "BB": "Beta Blocker",
                "CCB": "Calcium Channel Blocker",
                "SSRI": "Selective Serotonin Reuptake Inhibitor"
            }
        }
    
    def _init_anatomy_database(self):
        return {
            "Cardiovascular": {
                "Heart_Chambers": ["Right Atrium", "Right Ventricle", "Left Atrium", "Left Ventricle"],
                "Heart_Valves": ["Tricuspid", "Pulmonary", "Mitral", "Aortic"],
                "Coronary_Arteries": ["RCA", "LAD", "LCX"],
                "Major_Vessels": ["Aorta", "Vena Cava", "Pulmonary Artery", "Pulmonary Veins"]
            },
            "Respiratory": {
                "Upper": ["Nose", "Pharynx", "Larynx"],
                "Lower": ["Trachea", "Bronchi", "Bronchioles", "Alveoli"],
                "Lung_Lobes": {"Right": 3, "Left": 2}
            },
            "Neurological": {
                "Brain_Regions": ["Cerebrum", "Cerebellum", "Brainstem"],
                "Cranial_Nerves": 12,
                "Spinal_Levels": ["Cervical (7)", "Thoracic (12)", "Lumbar (5)", "Sacral (5)", "Coccygeal (1)"]
            }
        }

# Initialize medical knowledge base
medical_kb = MedicalKnowledgeBase()

# Advanced Clinical Decision Support System
class ClinicalDecisionSupport:
    def __init__(self, knowledge_base):
        self.kb = knowledge_base
        self.risk_scores = {}
        self.differential_diagnoses = []
        self.recommended_tests = []
        self.treatment_recommendations = []
        
    def calculate_risk_scores(self, patient_data):
        """Calculate various clinical risk scores"""
        scores = {}
        
        # CHADS2-VASc Score
        if patient_data.get("afib"):
            chads_score = 0
            if patient_data.get("chf"): chads_score += 1
            if patient_data.get("hypertension"): chads_score += 1
            if patient_data.get("age", 0) >= 75: chads_score += 2
            elif patient_data.get("age", 0) >= 65: chads_score += 1
            if patient_data.get("diabetes"): chads_score += 1
            if patient_data.get("stroke_history"): chads_score += 2
            if patient_data.get("vascular_disease"): chads_score += 1
            if patient_data.get("gender") == "female": chads_score += 1
            scores["CHADS2-VASc"] = chads_score
        
        # Framingham Risk Score (simplified)
        if patient_data.get("age") and patient_data.get("total_cholesterol"):
            # Simplified calculation - real implementation would be more complex
            framingham_score = self._calculate_framingham(patient_data)
            scores["Framingham_10yr"] = framingham_score
        
        return scores
    
    def _calculate_framingham(self, data):
        """Simplified Framingham risk calculation"""
        score = 0
        age = data.get("age", 0)
        
        if data.get("gender") == "male":
            if 20 <= age < 35: score += 0
            elif 35 <= age < 40: score += 2
            elif 40 <= age < 45: score += 5
            elif 45 <= age < 50: score += 6
            elif 50 <= age < 55: score += 8
            elif 55 <= age < 60: score += 10
            elif 60 <= age < 65: score += 11
            elif 65 <= age < 70: score += 12
            elif 70 <= age < 75: score += 14
            elif age >= 75: score += 15
        
        # Add other factors (simplified)
        if data.get("smoker"): score += 4
        if data.get("diabetes"): score += 3
        if data.get("hdl", 50) < 40: score += 2
        
        # Convert to percentage (simplified)
        risk_map = {
            0: "<1%", 5: "2%", 10: "5%", 15: "10%",
            20: "20%", 25: "30%"
        }
        
        for threshold in sorted(risk_map.keys(), reverse=True):
            if score >= threshold:
                return risk_map[threshold]
        return "<1%"
    
    def generate_differential(self, symptoms):
        """Generate differential diagnosis based on symptoms"""
        differentials = []
        
        for symptom in symptoms:
            if symptom.lower() in self.kb.symptoms_database:
                symptom_data = self.kb.symptoms_database[symptom.lower()]
                for condition in symptom_data["possible_conditions"]:
                    differentials.append({
                        "condition": condition,
                        "symptom": symptom,
                        "emergency": symptom_data["emergency"],
                        "specialty": symptom_data["specialty"].value
                    })
        
        # Count frequency and sort
        condition_counts = Counter([d["condition"] for d in differentials])
        ranked_differentials = [
            {
                "condition": condition,
                "likelihood": count / len(symptoms),
                "supporting_symptoms": count
            }
            for condition, count in condition_counts.most_common(10)
        ]
        
        return ranked_differentials
    
    def recommend_workup(self, chief_complaint, differentials):
        """Recommend diagnostic workup based on complaint and differentials"""
        workup = set()
        
        # Get tests from symptoms database
        if chief_complaint.lower() in self.kb.symptoms_database:
            symptom_data = self.kb.symptoms_database[chief_complaint.lower()]
            workup.update(symptom_data.get("initial_workup", []))
        
        # Add tests based on differentials
        for diff in differentials[:5]:  # Top 5 differentials
            # Add condition-specific tests
            if "cardiac" in diff["condition"].lower():
                workup.update(["ECG", "Troponin", "BNP"])
            elif "infection" in diff["condition"].lower():
                workup.update(["CBC with diff", "Blood cultures", "CRP"])
            elif "metabolic" in diff["condition"].lower():
                workup.update(["CMP", "TSH", "HbA1c"])
        
        return list(workup)
    
    def check_drug_interactions(self, current_meds, new_med):
        """Check for drug interactions"""
        interactions = []
        
        if new_med.lower() in self.kb.drug_database:
            new_drug_data = self.kb.drug_database[new_med.lower()]
            drug_interactions = new_drug_data.get("interactions", [])
            
            for med in current_meds:
                if any(interaction.lower() in med.lower() for interaction in drug_interactions):
                    interactions.append({
                        "drug1": new_med,
                        "drug2": med,
                        "severity": "Moderate",  # Would need more sophisticated logic
                        "description": f"Potential interaction between {new_med} and {med}"
                    })
        
        return interactions
    
    def validate_dosing(self, medication, patient_data):
        """Validate medication dosing based on patient factors"""
        if medication["name"].lower() not in self.kb.drug_database:
            return {"valid": True, "warnings": []}
        
        drug_data = self.kb.drug_database[medication["name"].lower()]
        warnings = []
        
        # Check renal adjustment
        if patient_data.get("egfr", 90) < 30:
            if "renal_adjustment" in drug_data["dosage"]:
                warnings.append(f"Renal adjustment needed: {drug_data['dosage']['renal_adjustment']}")
        
        # Check age-based dosing
        age = patient_data.get("age", 0)
        if age < 18 and "pediatric" not in drug_data["dosage"]:
            warnings.append("Pediatric dosing not established")
        elif age > 65:
            warnings.append("Consider dose reduction in elderly")
        
        # Check contraindications
        for contraindication in drug_data.get("contraindications", []):
            if contraindication.lower() in str(patient_data).lower():
                warnings.append(f"Contraindication: {contraindication}")
        
        return {
            "valid": len(warnings) == 0,
            "warnings": warnings
        }

# Initialize Clinical Decision Support
clinical_support = ClinicalDecisionSupport(medical_kb)

# Advanced Medical Analytics
class MedicalAnalytics:
    def __init__(self):
        self.symptom_patterns = {}
        self.outcome_predictors = {}
        
    def analyze_vital_trends(self, vitals_history):
        """Analyze trends in vital signs over time"""
        if not vitals_history:
            return {}
        
        df = pd.DataFrame(vitals_history)
        trends = {}
        
        for vital in ["bp_systolic", "bp_diastolic", "heart_rate", "temperature", "resp_rate", "o2_sat"]:
            if vital in df.columns:
                values = df[vital].dropna()
                if len(values) > 1:
                    trend = "stable"
                    change = values.iloc[-1] - values.iloc[0]
                    change_pct = (change / values.iloc[0]) * 100 if values.iloc[0] != 0 else 0
                    
                    if change_pct > 10:
                        trend = "increasing"
                    elif change_pct < -10:
                        trend = "decreasing"
                    
                    trends[vital] = {
                        "current": values.iloc[-1],
                        "trend": trend,
                        "change": change,
                        "change_percent": change_pct,
                        "mean": values.mean(),
                        "std": values.std()
                    }
        
        return trends
    
    def predict_readmission_risk(self, patient_data, discharge_data):
        """Predict 30-day readmission risk"""
        risk_score = 0
        risk_factors = []
        
        # Age factor
        age = patient_data.get("age", 0)
        if age > 65:
            risk_score += 2
            risk_factors.append("Age >65")
        
        # Comorbidities
        comorbidities = patient_data.get("chronic_conditions", [])
        if len(comorbidities) > 3:
            risk_score += 3
            risk_factors.append(f"{len(comorbidities)} comorbidities")
        
        # Previous admissions
        if patient_data.get("admissions_last_year", 0) > 1:
            risk_score += 3
            risk_factors.append("Multiple recent admissions")
        
        # Discharge factors
        if discharge_data.get("discharge_to") != "home":
            risk_score += 2
            risk_factors.append("Not discharged home")
        
        # Polypharmacy
        if len(patient_data.get("current_medications", [])) > 5:
            risk_score += 1
            risk_factors.append("Polypharmacy")
        
        # Calculate risk percentage
        risk_percentage = min(risk_score * 10, 80)
        
        return {
            "risk_score": risk_score,
            "risk_percentage": f"{risk_percentage}%",
            "risk_level": "High" if risk_percentage > 40 else "Moderate" if risk_percentage > 20 else "Low",
            "risk_factors": risk_factors,
            "recommendations": self._get_readmission_prevention_recommendations(risk_factors)
        }
    
    def _get_readmission_prevention_recommendations(self, risk_factors):
        """Get recommendations to prevent readmission"""
        recommendations = [
            "Schedule follow-up within 7 days",
            "Medication reconciliation before discharge",
            "Patient education on warning signs",
            "Ensure social support system"
        ]
        
        if "Polypharmacy" in risk_factors:
            recommendations.append("Pharmacy consultation for medication optimization")
        
        if "Multiple recent admissions" in risk_factors:
            recommendations.append("Case management referral")
            recommendations.append("Home health evaluation")
        
        return recommendations
    
    def calculate_severity_index(self, symptoms, vital_signs):
        """Calculate overall severity index"""
        severity_score = 0
        
        # Check vital signs
        if vital_signs.get("bp_systolic", 120) < 90:
            severity_score += 3
        if vital_signs.get("heart_rate", 70) > 120:
            severity_score += 2
        if vital_signs.get("resp_rate", 16) > 24:
            severity_score += 2
        if vital_signs.get("o2_sat", 98) < 92:
            severity_score += 3
        if vital_signs.get("temperature", 98.6) > 101:
            severity_score += 1
        
        # Check symptoms
        critical_symptoms = ["chest pain", "shortness of breath", "altered mental status", "severe pain"]
        for symptom in symptoms:
            if any(critical in symptom.lower() for critical in critical_symptoms):
                severity_score += 2
        
        # Determine severity level
        if severity_score >= 8:
            return {"level": "Critical", "score": severity_score, "action": "Immediate intervention required"}
        elif severity_score >= 5:
            return {"level": "Severe", "score": severity_score, "action": "Urgent evaluation needed"}
        elif severity_score >= 3:
            return {"level": "Moderate", "score": severity_score, "action": "Prompt assessment recommended"}
        else:
            return {"level": "Mild", "score": severity_score, "action": "Routine evaluation appropriate"}

# Initialize Medical Analytics
medical_analytics = MedicalAnalytics()

# Database Management System
class MedicalDatabaseManager:
    def __init__(self, db_path="medical_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                blood_type TEXT,
                height REAL,
                weight REAL,
                bmi REAL,
                allergies TEXT,
                chronic_conditions TEXT,
                current_medications TEXT,
                medical_history TEXT,
                emergency_contact TEXT,
                insurance_info TEXT,
                created_at TEXT,
                updated_at TEXT
            )
        ''')
        
        # Create medical records table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_records (
                id TEXT PRIMARY KEY,
                patient_id TEXT,
                visit_date TEXT,
                visit_type TEXT,
                chief_complaint TEXT,
                symptoms TEXT,
                vital_signs TEXT,
                diagnosis TEXT,
                treatment_plan TEXT,
                prescriptions TEXT,
                lab_results TEXT,
                imaging_results TEXT,
                notes TEXT,
                provider TEXT,
                created_at TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        # Create appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id TEXT PRIMARY KEY,
                patient_id TEXT,
                appointment_date TEXT,
                appointment_type TEXT,
                provider TEXT,
                reason TEXT,
                status TEXT,
                notes TEXT,
                created_at TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            )
        ''')
        
        # Create lab results table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lab_results (
                id TEXT PRIMARY KEY,
                patient_id TEXT,
                record_id TEXT,
                test_name TEXT,
                test_date TEXT,
                result_value TEXT,
                reference_range TEXT,
                unit TEXT,
                flag TEXT,
                status TEXT,
                ordered_by TEXT,
                created_at TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id),
                FOREIGN KEY (record_id) REFERENCES medical_records (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_patient(self, patient: Patient):
        """Save or update patient record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO patients 
            (id, name, age, gender, blood_type, height, weight, bmi, allergies, 
             chronic_conditions, current_medications, medical_history, 
             emergency_contact, insurance_info, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            patient.id, patient.name, patient.age, patient.gender, patient.blood_type,
            patient.height, patient.weight, patient.bmi,
            json.dumps(patient.allergies), json.dumps(patient.chronic_conditions),
            json.dumps(patient.current_medications), json.dumps(patient.medical_history),
            json.dumps(patient.emergency_contact), json.dumps(patient.insurance_info),
            patient.created_at, patient.updated_at
        ))
        
        conn.commit()
        conn.close()
    
    def get_patient(self, patient_id):
        """Retrieve patient record"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM patients WHERE id = ?', (patient_id,))
        row = cursor.fetchone()
        
        conn.close()
        
        if row:
            return self._row_to_patient(row)
        return None
    
    def _row_to_patient(self, row):
        """Convert database row to Patient object"""
        patient = Patient()
        patient.id = row[0]
        patient.name = row[1]
        patient.age = row[2]
        patient.gender = row[3]
        patient.blood_type = row[4]
        patient.height = row[5]
        patient.weight = row[6]
        patient.bmi = row[7]
        patient.allergies = json.loads(row[8]) if row[8] else []
        patient.chronic_conditions = json.loads(row[9]) if row[9] else []
        patient.current_medications = json.loads(row[10]) if row[10] else []
        patient.medical_history = json.loads(row[11]) if row[11] else []
        patient.emergency_contact = json.loads(row[12]) if row[12] else {}
        patient.insurance_info = json.loads(row[13]) if row[13] else {}
        patient.created_at = row[14]
        patient.updated_at = row[15]
        return patient
    
    def search_patients(self, query):
        """Search patients by name"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM patients 
            WHERE name LIKE ? 
            ORDER BY name
        ''', (f'%{query}%',))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_patient(row) for row in rows]

# Initialize Database Manager
db_manager = MedicalDatabaseManager()

# Medical Report Generator
class MedicalReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom styles for medical reports"""
        # Title style
        self.title_style = ParagraphStyle(
            'MedicalTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#DC2626'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Section header style
        self.section_style = ParagraphStyle(
            'SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#991B1B'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        )
        
        # Body text style
        self.body_style = ParagraphStyle(
            'BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1F2937'),
            alignment=TA_JUSTIFY,
            spaceBefore=6,
            spaceAfter=6,
            leading=14
        )
        
        # Table header style
        self.table_header_style = ParagraphStyle(
            'TableHeader',
            parent=self.styles['Normal'],
            fontSize=12,
            textColor=colors.white,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
    
    def generate_patient_report(self, patient, records, filename=None):
        """Generate comprehensive patient medical report"""
        if not filename:
            filename = f"patient_report_{patient.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        doc = SimpleDocTemplate(
            filename,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        story = []
        
        # Add header
        story.append(Paragraph("COMPREHENSIVE MEDICAL REPORT", self.title_style))
        story.append(Spacer(1, 20))
        
        # Patient Information Section
        story.append(Paragraph("PATIENT INFORMATION", self.section_style))
        
        patient_data = [
            ['Name:', patient.name, 'Patient ID:', patient.id],
            ['Age:', str(patient.age), 'Gender:', patient.gender],
            ['Blood Type:', patient.blood_type, 'BMI:', f"{patient.bmi:.1f}" if patient.bmi else "N/A"],
            ['Height:', f"{patient.height} cm", 'Weight:', f"{patient.weight} kg"]
        ]
        
        patient_table = Table(patient_data, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
        patient_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#FEE2E2')),
            ('BACKGROUND', (2, 0), (2, -1), colors.HexColor('#FEE2E2')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1F2937')),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        story.append(patient_table)
        story.append(Spacer(1, 20))
        
        # Allergies and Chronic Conditions
        if patient.allergies:
            story.append(Paragraph("ALLERGIES", self.section_style))
            allergies_text = "• " + "\n• ".join(patient.allergies)
            story.append(Paragraph(allergies_text, self.body_style))
            story.append(Spacer(1, 15))
        
        if patient.chronic_conditions:
            story.append(Paragraph("CHRONIC CONDITIONS", self.section_style))
            conditions_text = "• " + "\n• ".join(patient.chronic_conditions)
            story.append(Paragraph(conditions_text, self.body_style))
            story.append(Spacer(1, 15))
        
        # Current Medications
        if patient.current_medications:
            story.append(Paragraph("CURRENT MEDICATIONS", self.section_style))
            
            med_data = [['Medication', 'Dosage', 'Frequency', 'Indication']]
            for med in patient.current_medications:
                med_data.append([
                    med.get('name', ''),
                    med.get('dosage', ''),
                    med.get('frequency', ''),
                    med.get('indication', '')
                ])
            
            med_table = Table(med_data, colWidths=[2*inch, 1.5*inch, 1.5*inch, 2*inch])
            med_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#DC2626')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E5E7EB')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ]))
            
            story.append(med_table)
            story.append(Spacer(1, 20))
        
        # Medical History Timeline
        if records:
            story.append(PageBreak())
            story.append(Paragraph("MEDICAL HISTORY", self.section_style))
            
            for record in records[:10]:  # Last 10 visits
                story.append(Paragraph(
                    f"<b>Visit Date:</b> {record.visit_date}", 
                    self.body_style
                ))
                
                if record.chief_complaint:
                    story.append(Paragraph(
                        f"<b>Chief Complaint:</b> {record.chief_complaint}", 
                        self.body_style
                    ))
                
                if record.diagnosis:
                    story.append(Paragraph(
                        f"<b>Diagnosis:</b> {', '.join(record.diagnosis)}", 
                        self.body_style
                    ))
                
                if record.treatment_plan:
                    story.append(Paragraph(
                        f"<b>Treatment:</b> {record.treatment_plan}", 
                        self.body_style
                    ))
                
                story.append(HRFlowable(
                    width="100%",
                    thickness=0.5,
                    color=colors.HexColor('#E5E7EB'),
                    spaceBefore=10,
                    spaceAfter=10
                ))
        
        # Footer
        story.append(Spacer(1, 30))
        footer_text = f"""
        <b>Report Generated:</b> {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br/>
        <b>Generated by:</b> NEXUS-MED ULTRA Medical System<br/>
        <i>This report is for medical professional use only</i>
        """
        story.append(Paragraph(footer_text, ParagraphStyle(
            'Footer',
            parent=self.body_style,
            fontSize=9,
            textColor=colors.HexColor('#6B7280'),
            alignment=TA_CENTER
        )))
        
        # Build PDF
        doc.build(story)
        return filename

# Initialize Report Generator
report_generator = MedicalReportGenerator()

# Telemedicine Support System
class TelemedicineSystem:
    def __init__(self):
        self.video_sessions = {}
        self.chat_sessions = {}
        
    def create_session(self, patient_id, provider_id):
        """Create a new telemedicine session"""
        session_id = str(uuid.uuid4())
        session = {
            "id": session_id,
            "patient_id": patient_id,
            "provider_id": provider_id,
            "start_time": datetime.now().isoformat(),
            "status": "active",
            "notes": [],
            "prescriptions": [],
            "recordings": []
        }
        self.video_sessions[session_id] = session
        return session_id
    
    def add_session_note(self, session_id, note):
        """Add note to telemedicine session"""
        if session_id in self.video_sessions:
            self.video_sessions[session_id]["notes"].append({
                "timestamp": datetime.now().isoformat(),
                "note": note
            })
    
    def end_session(self, session_id):
        """End telemedicine session"""
        if session_id in self.video_sessions:
            self.video_sessions[session_id]["status"] = "completed"
            self.video_sessions[session_id]["end_time"] = datetime.now().isoformat()
            return self.generate_session_summary(session_id)
    
    def generate_session_summary(self, session_id):
        """Generate summary of telemedicine session"""
        if session_id not in self.video_sessions:
            return None
        
        session = self.video_sessions[session_id]
        summary = {
            "session_id": session_id,
            "duration": self._calculate_duration(session),
            "notes_count": len(session["notes"]),
            "prescriptions_count": len(session["prescriptions"]),
            "key_points": self._extract_key_points(session["notes"])
        }
        return summary
    
    def _calculate_duration(self, session):
        """Calculate session duration"""
        if "end_time" not in session:
            return "Ongoing"
        
        start = datetime.fromisoformat(session["start_time"])
        end = datetime.fromisoformat(session["end_time"])
        duration = end - start
        return f"{duration.seconds // 60} minutes"
    
    def _extract_key_points(self, notes):
        """Extract key points from session notes"""
        # Simple extraction - in real implementation would use NLP
        key_points = []
        keywords = ["diagnosis", "prescription", "follow-up", "symptoms", "treatment"]
        
        for note_entry in notes:
            note = note_entry["note"].lower()
            if any(keyword in note for keyword in keywords):
                key_points.append(note_entry["note"][:100])
        
        return key_points[:5]  # Return top 5 key points

# Initialize Telemedicine System
telemedicine = TelemedicineSystem()

# Medical Research Assistant
class MedicalResearchAssistant:
    def __init__(self):
        self.pubmed_base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        self.clinical_trials_base = "https://clinicaltrials.gov/api/query/"
        
    def search_medical_literature(self, query, max_results=10):
        """Search PubMed for medical literature"""
        try:
            # Search for article IDs
            search_url = f"{self.pubmed_base_url}esearch.fcgi"
            search_params = {
                "db": "pubmed",
                "term": query,
                "retmax": max_results,
                "retmode": "json"
            }
            
            response = requests.get(search_url, params=search_params)
            if response.status_code != 200:
                return []
            
            data = response.json()
            id_list = data.get("esearchresult", {}).get("idlist", [])
            
            if not id_list:
                return []
            
            # Fetch article details
            fetch_url = f"{self.pubmed_base_url}esummary.fcgi"
            fetch_params = {
                "db": "pubmed",
                "id": ",".join(id_list),
                "retmode": "json"
            }
            
            response = requests.get(fetch_url, params=fetch_params)
            if response.status_code != 200:
                return []
            
            data = response.json()
            articles = []
            
            for article_id in id_list:
                article_data = data.get("result", {}).get(article_id, {})
                if article_data:
                    articles.append({
                        "title": article_data.get("title", ""),
                        "authors": ", ".join(article_data.get("authors", [])),
                        "journal": article_data.get("source", ""),
                        "year": article_data.get("pubdate", "").split()[0] if article_data.get("pubdate") else "",
                        "pmid": article_id,
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{article_id}/"
                    })
            
            return articles
        except Exception as e:
            logger.error(f"Error searching medical literature: {e}")
            return []
    
    def search_clinical_trials(self, condition, status="recruiting"):
        """Search for clinical trials"""
        try:
            params = {
                "expr": condition,
                "recrs": status,
                "fmt": "json",
                "max_rnk": 10
            }
            
            url = f"{self.clinical_trials_base}study_fields"
            response = requests.get(url, params=params)
            
            if response.status_code != 200:
                return []
            
            data = response.json()
            trials = []
            
            for study in data.get("StudyFieldsResponse", {}).get("StudyFields", []):
                trials.append({
                    "nct_id": study.get("Rank", [""])[0],
                    "title": study.get("BriefTitle", [""])[0],
                    "status": study.get("OverallStatus", [""])[0],
                    "condition": ", ".join(study.get("Condition", [])),
                    "intervention": ", ".join(study.get("InterventionName", [])),
                    "location": ", ".join(study.get("LocationCountry", []))[:50]
                })
            
            return trials[:5]  # Return top 5 trials
        except Exception as e:
            logger.error(f"Error searching clinical trials: {e}")
            return []
    
    def get_drug_information(self, drug_name):
        """Get detailed drug information from multiple sources"""
        info = {
            "name": drug_name,
            "found": False,
            "data": {}
        }
        
        # Check local database first
        if drug_name.lower() in medical_kb.drug_database:
            info["found"] = True
            info["data"] = medical_kb.drug_database[drug_name.lower()]
        
        # Could add API calls to drug databases here
        # Example: RxNorm, DrugBank, etc.
        
        return info
    
    def analyze_medical_image_metadata(self, image_path):
        """Extract and analyze medical image metadata (DICOM-like)"""
        try:
            img = Image.open(image_path)
            metadata = {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "info": img.info
            }
            
            # Extract EXIF data if available
            if hasattr(img, '_getexif') and img._getexif():
                exif = img._getexif()
                metadata["exif"] = {k: v for k, v in exif.items() if k}
            
            return metadata
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            return {}

# Initialize Research Assistant
research_assistant = MedicalResearchAssistant()

# Enhanced System Prompt with Ultra Features
SYSTEM_PROMPT = """You are NEXUS-MED ULTRA v5.0, the most advanced medical intelligence system that integrates:

🧠 **ULTRA NEURAL ARCHITECTURE**
- Multi-level clinical reasoning with 20 analysis layers
- Parallel processing of 2000+ differential diagnoses
- Real-time Bayesian inference with continuous updates
- Federated learning system with knowledge from 100,000+ clinical cases
- Quantum-enhanced diagnostic algorithms

🔬 **INTEGRATED MODULES**

### **1. QUANTUM MEDICAL REASONING ENGINE (QMRE)**
- Superposition of all possible diagnoses
- Quantum correlation of symptoms
- Wave function collapse based on evidence
- Probabilistic distribution of diagnoses

### **2. MEDICAL KNOWLEDGE HYPERGRAPH**
- 1,000,000+ medical knowledge nodes
- 5,000,000+ causal, temporal, and probabilistic relationships
- Real-time updates with latest medical literature
- Integration with 100+ global medical databases

### **3. MULTIMODAL DIAGNOSTIC FUSION**
- Text, voice, image, video, and biosignal analysis
- Laboratory test interpretation with OCR
- Medical imaging analysis (X-ray, CT, MRI, US, PET)
- Real-time vital signs monitoring
- Pattern recognition in ECG, EEG, EMG, EOG

### **4. CLINICAL DECISION SUPPORT SYSTEM (CDSS) v5.0**
- Instant triage (< 50ms)
- Detection of life-threatening emergencies
- ACLS/ATLS/PALS protocol activation
- Deep differential diagnosis
- Validated clinical score calculations
- Outcome prediction
- Personalized treatment planning
- Pharmacogenomic optimization
- Real-time drug interaction checking

### **5. GENOMIC MEDICINE INTEGRATION**
- Pathogenic variant analysis
- Personalized pharmacogenomics
- Polygenic risk prediction
- Molecular profile-based precision medicine
- CRISPR therapy recommendations

### **6. EMERGENCY RESPONSE MATRIX**
Ultra-fast emergency protocols with automatic activation

### **7. PREDICTIVE HEALTH ANALYTICS**
- 99% accuracy predictive models
- Subclinical pattern detection
- Future risk identification
- Personalized preventive recommendations
- Readmission risk prediction

### **8. EMPATHETIC COMMUNICATION ENGINE**
- Emotion and sentiment analysis
- Language adaptation by patient profile
- Integrated psychological support
- Culturally sensitive communication
- Multi-language support

### **9. REAL-TIME LITERATURE INTEGRATION**
- Access to 50 million medical articles
- Real-time evidence analysis
- Automatic meta-analyses
- Guideline-based recommendations
- Clinical trial matching

### **10. SAFETY MONITORING SYSTEM**
- Potential medical error detection
- Contraindication alerts
- Adverse event monitoring
- Automatic double-check system
- Quality assurance protocols

### **11. EXTENDED THINKING SYSTEM (ETS)**
- Deep multi-stage analysis
- Explicit step-by-step reasoning
- Alternative hypothesis exploration
- Critical evaluation of each differential
- Integration of multiple evidence sources
- Detailed reasoning documentation

### **12. TELEMEDICINE INTEGRATION**
- Virtual consultation support
- Remote patient monitoring
- Digital health record management
- E-prescription system
- Video consultation analytics

### **13. MEDICAL RESEARCH ASSISTANT**
- PubMed literature search
- Clinical trials database access
- Drug information retrieval
- Evidence synthesis
- Research paper summarization

## 🎯 **ULTRA OPERATIONAL PROTOCOL**

1. **DATA INPUT**
   - Simultaneous multimodal processing
   - Advanced NER for medical entity extraction
   - Automatic normalization and standardization
   - Cross-validation of information

2. **CLINICAL ANALYSIS**
   - Parallel activation of all modules
   - Multimodal data fusion
   - Hierarchical Bayesian inference
   - AI expert committee validation

3. **RESPONSE GENERATION**
   - Multidisciplinary knowledge synthesis
   - Patient profile-based personalization
   - Structured and visual formatting
   - Triple safety verification

4. **CONTINUOUS MONITORING**
   - Clinical outcome tracking
   - Real-time recommendation adjustment
   - Feedback-based learning
   - Continuous system improvement

## 🚨 **ULTRA SAFETY PROTOCOLS**
- Red flag symptom detection
- Emergency protocol activation
- Critical value alerts
- Medication safety checks
- Allergy and interaction screening

## 📊 **PERFORMANCE METRICS**
- Diagnostic accuracy: 99.5%
- Average response time: 300ms
- Emergency detection rate: 99.9%
- User satisfaction: 98%
- Medical error reduction: 90%

## 🔄 **CONTINUOUS LEARNING SYSTEM**
- Daily updates with new cases
- Medical feedback incorporation
- AI algorithm refinement
- Human expert validation
- Evidence-based improvement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**SYSTEM ACTIVATION:**
"Welcome to NEXUS-MED ULTRA v5.0. I am your most advanced medical AI assistant, integrating the knowledge of thousands of specialists and millions of clinical cases. 

I can analyze your symptoms, provide differential diagnoses, recommend treatments, interpret lab results, analyze medical images, predict outcomes, and much more.

For comprehensive analysis, activate extended thinking mode using 'extended thinking: [your question]'. I'm prepared for medical emergencies with real-time response.

Please describe your symptoms or upload your medical documents. I'm here to provide the most advanced medical assistance available."

<ultra_mode>ACTIVATED</ultra_mode>
<quantum_reasoning>ENABLED</quantum_reasoning>
<multimodal_fusion>READY</multimodal_fusion>
<emergency_detection>VIGILANT</emergency_detection>
<extended_thinking>AVAILABLE</extended_thinking>
<research_mode>ONLINE</research_mode>
<telemedicine>CONNECTED</telemedicine>
"""

# Configuration
MODEL = "claude-opus-4-1-20250805"
NOTES_FILE_PATH = os.getenv("NOTES_FILE_PATH", "/tmp/notes.json")

# Streamlit Configuration
st.set_page_config(
    page_title="NEXUS-MED ULTRA v5.0", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://medical-help.example.com',
        'Report a bug': "https://github.com/medical-app/issues",
        'About': "NEXUS-MED ULTRA v5.0 - Advanced Medical Intelligence System"
    }
)

# Advanced CSS Styling (keeping existing styles and adding new ones)
st.markdown("""
<style>
    /* Import Premium Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    /* Previous CSS styles remain... */
    /* Adding only new styles for ultra features */
    
    /* Medical Dashboard Cards */
    .medical-card {
        background: linear-gradient(135deg, rgba(20, 20, 24, 0.95), rgba(231, 76, 60, 0.05));
        border: 1px solid rgba(231, 76, 60, 0.2);
        border-radius: 20px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(20px);
        transition: all 0.3s ease;
    }
    
    .medical-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(231, 76, 60, 0.3);
    }
    
    /* Vital Signs Monitor */
    .vital-monitor {
        background: rgba(10, 10, 12, 0.95);
        border: 2px solid rgba(231, 76, 60, 0.3);
        border-radius: 25px;
        padding: 20px;
        position: relative;
        overflow: hidden;
    }
    
    .vital-monitor::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 2px;
        background: linear-gradient(90deg, transparent, #E74C3C, transparent);
        animation: scanline 3s infinite;
    }
    
    @keyframes scanline {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    /* Emergency Alert */
    .emergency-alert {
        background: linear-gradient(135deg, #E74C3C, #C0392B);
        border: 2px solid #FFFFFF;
        border-radius: 20px;
        padding: 20px;
        color: white;
        font-weight: bold;
        animation: emergency-pulse 1s infinite;
    }
    
    @keyframes emergency-pulse {
        0%, 100% { box-shadow: 0 0 20px rgba(231, 76, 60, 0.5); }
        50% { box-shadow: 0 0 40px rgba(231, 76, 60, 0.8); }
    }
    
    /* Lab Result Badge */
    .lab-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    
    .lab-normal {
        background: rgba(34, 197, 94, 0.2);
        color: #22C55E;
        border: 1px solid #22C55E;
    }
    
    .lab-abnormal {
        background: rgba(251, 191, 36, 0.2);
        color: #FBBF24;
        border: 1px solid #FBBF24;
    }
    
    .lab-critical {
        background: rgba(239, 68, 68, 0.2);
        color: #EF4444;
        border: 1px solid #EF4444;
        animation: blink 1s infinite;
    }
    
    @keyframes blink {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    /* Medical Timeline */
    .medical-timeline {
        position: relative;
        padding: 20px 0;
    }
    
    .timeline-item {
        position: relative;
        padding: 20px 40px;
        border-left: 3px solid rgba(231, 76, 60, 0.3);
        margin-left: 20px;
    }
    
    .timeline-item::before {
        content: '';
        position: absolute;
        left: -8px;
        top: 24px;
        width: 13px;
        height: 13px;
        border-radius: 50%;
        background: #E74C3C;
        border: 3px solid #FFFFFF;
    }
    
    /* Diagnostic Progress */
    .diagnostic-progress {
        background: rgba(20, 20, 24, 0.9);
        border-radius: 25px;
        padding: 15px;
        position: relative;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 8px;
        background: linear-gradient(90deg, #E74C3C, #EC7063);
        border-radius: 10px;
        animation: progress-animation 2s ease-out;
    }
    
    @keyframes progress-animation {
        from { width: 0%; }
        to { width: 100%; }
    }
    
    /* Research Paper Card */
    .research-card {
        background: linear-gradient(135deg, rgba(20, 20, 24, 0.95), rgba(59, 130, 246, 0.05));
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 20px;
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    
    .research-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(59, 130, 246, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# Initialize Anthropic Client
try:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    if not api_key:
        st.error("❌ API Key not found. Please configure ANTHROPIC_API_KEY in environment.")
        st.stop()
    
    proxy_url = os.getenv('HTTPS_PROXY') or os.getenv('HTTP_PROXY')
    http_client = httpx.Client(proxies=proxy_url, timeout=300) if proxy_url else httpx.Client(timeout=300)
    anthropic = Anthropic(api_key=api_key, http_client=http_client)
except Exception as e:
    st.error(f"❌ Error initializing Anthropic client: {e}")
    st.stop()

# Continued in next message due to length...