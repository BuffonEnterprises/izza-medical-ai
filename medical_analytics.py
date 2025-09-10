#!/usr/bin/env python3
"""
NEXUS-MED ULTRA - Medical Analytics Module
Advanced medical data analysis and visualization system
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
import json

# Try to import ML libraries
try:
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    from sklearn.decomposition import PCA
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import accuracy_score, confusion_matrix
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False

logger = logging.getLogger(__name__)

@dataclass
class VitalSignsTrend:
    """Data class for vital signs trends"""
    timestamps: List[str]
    heart_rate: List[float]
    blood_pressure_sys: List[float]
    blood_pressure_dia: List[float]
    temperature: List[float]
    respiratory_rate: List[float]
    spo2: List[float]

class MedicalAnalytics:
    """Advanced medical analytics engine"""
    
    def __init__(self):
        self.setup_plotting_style()
    
    def setup_plotting_style(self):
        """Setup consistent plotting style"""
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def analyze_vital_signs_trends(self, vital_signs_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze vital signs trends and detect anomalies"""
        if not vital_signs_data:
            return {"error": "No vital signs data available"}
        
        # Convert to DataFrame
        df = pd.DataFrame(vital_signs_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Calculate statistics
        stats = {
            'heart_rate': {
                'mean': df['heart_rate'].mean(),
                'std': df['heart_rate'].std(),
                'min': df['heart_rate'].min(),
                'max': df['heart_rate'].max(),
                'trend': self._calculate_trend(df['heart_rate'])
            },
            'blood_pressure': {
                'systolic_mean': df['bp_systolic'].mean(),
                'diastolic_mean': df['bp_diastolic'].mean(),
                'pulse_pressure': (df['bp_systolic'] - df['bp_diastolic']).mean(),
                'hypertension_episodes': len(df[df['bp_systolic'] > 140])
            },
            'temperature': {
                'mean': df['temperature'].mean(),
                'fever_episodes': len(df[df['temperature'] > 37.5]),
                'hypothermia_episodes': len(df[df['temperature'] < 36.0])
            },
            'respiratory': {
                'mean': df['respiratory_rate'].mean(),
                'tachypnea_episodes': len(df[df['respiratory_rate'] > 20]),
                'bradypnea_episodes': len(df[df['respiratory_rate'] < 12])
            },
            'oxygen': {
                'mean': df['spo2'].mean(),
                'hypoxia_episodes': len(df[df['spo2'] < 92]),
                'severe_hypoxia_episodes': len(df[df['spo2'] < 88])
            }
        }
        
        # Detect anomalies
        anomalies = self._detect_vital_signs_anomalies(df)
        
        # Calculate risk scores
        risk_scores = self._calculate_risk_scores(df)
        
        return {
            'statistics': stats,
            'anomalies': anomalies,
            'risk_scores': risk_scores,
            'dataframe': df
        }
    
    def _calculate_trend(self, series: pd.Series) -> str:
        """Calculate trend direction"""
        if len(series) < 2:
            return "insufficient_data"
        
        # Simple linear regression slope
        x = np.arange(len(series))
        slope = np.polyfit(x, series.values, 1)[0]
        
        if abs(slope) < 0.1:
            return "stable"
        elif slope > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def _detect_vital_signs_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Detect anomalies in vital signs"""
        anomalies = []
        
        # Define normal ranges
        normal_ranges = {
            'heart_rate': (60, 100),
            'bp_systolic': (90, 140),
            'bp_diastolic': (60, 90),
            'temperature': (36.5, 37.5),
            'respiratory_rate': (12, 20),
            'spo2': (95, 100)
        }
        
        for idx, row in df.iterrows():
            row_anomalies = []
            
            # Check each vital sign
            if not (normal_ranges['heart_rate'][0] <= row['heart_rate'] <= normal_ranges['heart_rate'][1]):
                row_anomalies.append({
                    'type': 'heart_rate',
                    'value': row['heart_rate'],
                    'severity': 'high' if abs(row['heart_rate'] - 80) > 40 else 'medium'
                })
            
            if not (normal_ranges['bp_systolic'][0] <= row['bp_systolic'] <= normal_ranges['bp_systolic'][1]):
                row_anomalies.append({
                    'type': 'blood_pressure',
                    'value': f"{row['bp_systolic']}/{row['bp_diastolic']}",
                    'severity': 'high' if row['bp_systolic'] > 180 else 'medium'
                })
            
            if not (normal_ranges['temperature'][0] <= row['temperature'] <= normal_ranges['temperature'][1]):
                row_anomalies.append({
                    'type': 'temperature',
                    'value': row['temperature'],
                    'severity': 'high' if row['temperature'] > 39 or row['temperature'] < 35 else 'medium'
                })
            
            if not (normal_ranges['spo2'][0] <= row['spo2'] <= normal_ranges['spo2'][1]):
                row_anomalies.append({
                    'type': 'oxygen_saturation',
                    'value': row['spo2'],
                    'severity': 'critical' if row['spo2'] < 88 else 'high'
                })
            
            if row_anomalies:
                anomalies.append({
                    'timestamp': row['timestamp'].isoformat(),
                    'anomalies': row_anomalies
                })
        
        return anomalies
    
    def _calculate_risk_scores(self, df: pd.DataFrame) -> Dict[str, float]:
        """Calculate various risk scores based on vital signs"""
        risk_scores = {}
        
        # Early Warning Score (EWS)
        ews_score = 0
        latest = df.iloc[-1]
        
        # Heart rate scoring
        if latest['heart_rate'] < 40 or latest['heart_rate'] > 130:
            ews_score += 3
        elif latest['heart_rate'] < 51 or latest['heart_rate'] > 110:
            ews_score += 2
        elif latest['heart_rate'] < 60 or latest['heart_rate'] > 100:
            ews_score += 1
        
        # Systolic BP scoring
        if latest['bp_systolic'] < 70 or latest['bp_systolic'] > 219:
            ews_score += 3
        elif latest['bp_systolic'] < 81 or latest['bp_systolic'] > 199:
            ews_score += 2
        elif latest['bp_systolic'] < 91 or latest['bp_systolic'] > 179:
            ews_score += 1
        
        # Temperature scoring
        if latest['temperature'] < 35.0 or latest['temperature'] > 38.9:
            ews_score += 2
        elif latest['temperature'] < 36.0 or latest['temperature'] > 38.0:
            ews_score += 1
        
        # Respiratory rate scoring
        if latest['respiratory_rate'] < 9 or latest['respiratory_rate'] > 29:
            ews_score += 3
        elif latest['respiratory_rate'] > 24:
            ews_score += 2
        elif latest['respiratory_rate'] < 12 or latest['respiratory_rate'] > 20:
            ews_score += 1
        
        # SpO2 scoring
        if latest['spo2'] < 85:
            ews_score += 3
        elif latest['spo2'] < 90:
            ews_score += 2
        elif latest['spo2'] < 94:
            ews_score += 1
        
        risk_scores['early_warning_score'] = ews_score
        risk_scores['risk_level'] = self._classify_risk_level(ews_score)
        
        # Calculate trend-based risk
        if len(df) > 5:
            hr_trend = df['heart_rate'].tail(5).pct_change().mean()
            bp_trend = df['bp_systolic'].tail(5).pct_change().mean()
            
            if abs(hr_trend) > 0.1 or abs(bp_trend) > 0.1:
                risk_scores['trend_risk'] = 'increasing'
            else:
                risk_scores['trend_risk'] = 'stable'
        
        return risk_scores
    
    def _classify_risk_level(self, ews_score: int) -> str:
        """Classify risk level based on EWS score"""
        if ews_score >= 7:
            return "critical"
        elif ews_score >= 5:
            return "high"
        elif ews_score >= 3:
            return "medium"
        elif ews_score >= 1:
            return "low"
        else:
            return "minimal"
    
    def create_vital_signs_dashboard(self, vital_signs_data: List[Dict[str, Any]]) -> go.Figure:
        """Create interactive vital signs dashboard"""
        if not vital_signs_data:
            return None
        
        df = pd.DataFrame(vital_signs_data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.sort_values('timestamp')
        
        # Create subplots
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=('Heart Rate', 'Blood Pressure', 'Temperature',
                          'Respiratory Rate', 'SpO2', 'Risk Score Trend'),
            vertical_spacing=0.1,
            horizontal_spacing=0.1
        )
        
        # Heart Rate
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['heart_rate'],
                      mode='lines+markers', name='Heart Rate',
                      line=dict(color='red', width=2)),
            row=1, col=1
        )
        fig.add_hrect(y0=60, y1=100, fillcolor="green", opacity=0.1,
                     layer="below", line_width=0, row=1, col=1)
        
        # Blood Pressure
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['bp_systolic'],
                      mode='lines+markers', name='Systolic',
                      line=dict(color='darkblue', width=2)),
            row=1, col=2
        )
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['bp_diastolic'],
                      mode='lines+markers', name='Diastolic',
                      line=dict(color='lightblue', width=2)),
            row=1, col=2
        )
        
        # Temperature
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['temperature'],
                      mode='lines+markers', name='Temperature',
                      line=dict(color='orange', width=2)),
            row=2, col=1
        )
        fig.add_hrect(y0=36.5, y1=37.5, fillcolor="green", opacity=0.1,
                     layer="below", line_width=0, row=2, col=1)
        
        # Respiratory Rate
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['respiratory_rate'],
                      mode='lines+markers', name='Resp Rate',
                      line=dict(color='purple', width=2)),
            row=2, col=2
        )
        
        # SpO2
        fig.add_trace(
            go.Scatter(x=df['timestamp'], y=df['spo2'],
                      mode='lines+markers', name='SpO2',
                      line=dict(color='green', width=2)),
            row=3, col=1
        )
        fig.add_hrect(y0=95, y1=100, fillcolor="green", opacity=0.1,
                     layer="below", line_width=0, row=3, col=1)
        
        # Update layout
        fig.update_layout(
            title="Vital Signs Dashboard",
            showlegend=True,
            height=800,
            template="plotly_white"
        )
        
        # Update y-axis labels
        fig.update_yaxes(title_text="BPM", row=1, col=1)
        fig.update_yaxes(title_text="mmHg", row=1, col=2)
        fig.update_yaxes(title_text="°C", row=2, col=1)
        fig.update_yaxes(title_text="Breaths/min", row=2, col=2)
        fig.update_yaxes(title_text="%", row=3, col=1)
        
        return fig
    
    def predict_readmission_risk(self, patient_data: Dict[str, Any]) -> Dict[str, Any]:
        """Predict 30-day readmission risk using ML"""
        if not ML_AVAILABLE:
            return {"error": "ML libraries not available"}
        
        # Extract features
        features = self._extract_readmission_features(patient_data)
        
        # Simple rule-based model for demonstration
        risk_score = 0
        
        # Age factor
        age = patient_data.get('age', 0)
        if age > 65:
            risk_score += 2
        elif age > 50:
            risk_score += 1
        
        # Chronic conditions
        chronic_conditions = patient_data.get('chronic_conditions', [])
        risk_score += len(chronic_conditions) * 0.5
        
        # Recent hospitalizations
        recent_records = patient_data.get('recent_records', [])
        if len(recent_records) > 2:
            risk_score += 2
        
        # Calculate probability
        probability = min(risk_score / 10, 0.95)
        
        return {
            'risk_score': risk_score,
            'probability': probability,
            'risk_level': 'high' if probability > 0.5 else 'medium' if probability > 0.3 else 'low',
            'factors': self._identify_risk_factors(patient_data)
        }
    
    def _extract_readmission_features(self, patient_data: Dict[str, Any]) -> np.ndarray:
        """Extract features for readmission prediction"""
        features = []
        
        # Demographics
        features.append(patient_data.get('age', 0))
        features.append(1 if patient_data.get('gender') == 'Male' else 0)
        
        # Medical history
        features.append(len(patient_data.get('chronic_conditions', [])))
        features.append(len(patient_data.get('allergies', [])))
        features.append(len(patient_data.get('current_medications', [])))
        
        # Recent vitals (if available)
        latest_vitals = patient_data.get('latest_vitals', {})
        features.append(latest_vitals.get('heart_rate', 75))
        features.append(latest_vitals.get('bp_systolic', 120))
        features.append(latest_vitals.get('spo2', 98))
        
        return np.array(features)
    
    def _identify_risk_factors(self, patient_data: Dict[str, Any]) -> List[str]:
        """Identify specific risk factors for readmission"""
        risk_factors = []
        
        if patient_data.get('age', 0) > 65:
            risk_factors.append("Age > 65 years")
        
        chronic_conditions = patient_data.get('chronic_conditions', [])
        if 'diabetes' in [c.lower() for c in chronic_conditions]:
            risk_factors.append("Diabetes mellitus")
        if 'heart' in ' '.join(chronic_conditions).lower():
            risk_factors.append("Cardiac condition")
        
        if len(patient_data.get('current_medications', [])) > 5:
            risk_factors.append("Polypharmacy (>5 medications)")
        
        return risk_factors
    
    def generate_clinical_summary(self, patient_data: Dict[str, Any], 
                                 analytics_results: Dict[str, Any]) -> str:
        """Generate a clinical summary based on analytics"""
        summary = []
        
        # Patient overview
        summary.append(f"**Patient Overview**")
        summary.append(f"- Age: {patient_data.get('age')} years")
        summary.append(f"- Gender: {patient_data.get('gender')}")
        
        # Vital signs summary
        if 'statistics' in analytics_results:
            stats = analytics_results['statistics']
            summary.append("\n**Vital Signs Summary**")
            summary.append(f"- Heart Rate: {stats['heart_rate']['mean']:.1f} bpm (trend: {stats['heart_rate']['trend']})")
            summary.append(f"- Blood Pressure: {stats['blood_pressure']['systolic_mean']:.0f}/{stats['blood_pressure']['diastolic_mean']:.0f} mmHg")
            summary.append(f"- Temperature: {stats['temperature']['mean']:.1f}°C")
            summary.append(f"- SpO2: {stats['oxygen']['mean']:.1f}%")
        
        # Risk assessment
        if 'risk_scores' in analytics_results:
            risk = analytics_results['risk_scores']
            summary.append("\n**Risk Assessment**")
            summary.append(f"- Early Warning Score: {risk['early_warning_score']}")
            summary.append(f"- Risk Level: {risk['risk_level'].upper()}")
        
        # Anomalies
        if 'anomalies' in analytics_results and analytics_results['anomalies']:
            summary.append("\n**Notable Findings**")
            for anomaly in analytics_results['anomalies'][:3]:  # Show top 3
                summary.append(f"- {anomaly['timestamp']}: {', '.join([a['type'] for a in anomaly['anomalies']])}")
        
        return '\n'.join(summary)
    
    def create_lab_results_visualization(self, lab_results: List[Dict[str, Any]]) -> go.Figure:
        """Create visualization for lab results trends"""
        if not lab_results:
            return None
        
        # Group by test name
        df = pd.DataFrame(lab_results)
        test_groups = df.groupby('test_name')
        
        # Create figure with subplots for each test
        n_tests = len(test_groups)
        fig = make_subplots(
            rows=n_tests, cols=1,
            subplot_titles=[name for name, _ in test_groups],
            vertical_spacing=0.05
        )
        
        for i, (test_name, group) in enumerate(test_groups, 1):
            # Convert test_date to datetime
            group['test_date'] = pd.to_datetime(group['test_date'])
            group = group.sort_values('test_date')
            
            # Add trace
            fig.add_trace(
                go.Scatter(
                    x=group['test_date'],
                    y=group['result_value'].astype(float),
                    mode='lines+markers',
                    name=test_name,
                    showlegend=False
                ),
                row=i, col=1
            )
            
            # Add reference range if available
            if 'reference_range' in group.columns and not group['reference_range'].isna().all():
                ref_range = group['reference_range'].iloc[0]
                if '-' in str(ref_range):
                    try:
                        low, high = map(float, ref_range.split('-'))
                        fig.add_hrect(
                            y0=low, y1=high,
                            fillcolor="green", opacity=0.1,
                            layer="below", line_width=0,
                            row=i, col=1
                        )
                    except:
                        pass
        
        fig.update_layout(
            title="Lab Results Trends",
            height=200 * n_tests,
            showlegend=False
        )
        
        return fig
    
    def calculate_medication_interactions_risk(self, medications: List[str]) -> Dict[str, Any]:
        """Calculate potential drug interaction risks"""
        # Simplified interaction database
        known_interactions = {
            ('warfarin', 'aspirin'): 'high',
            ('ace_inhibitor', 'potassium'): 'medium',
            ('metformin', 'contrast'): 'high',
            ('ssri', 'nsaid'): 'medium'
        }
        
        interactions = []
        risk_level = 'low'
        
        # Check for interactions (simplified)
        for i, med1 in enumerate(medications):
            for med2 in medications[i+1:]:
                # Check if drugs interact
                for (drug1, drug2), severity in known_interactions.items():
                    if (drug1 in med1.lower() and drug2 in med2.lower()) or \
                       (drug2 in med1.lower() and drug1 in med2.lower()):
                        interactions.append({
                            'drug1': med1,
                            'drug2': med2,
                            'severity': severity
                        })
                        if severity == 'high':
                            risk_level = 'high'
                        elif severity == 'medium' and risk_level != 'high':
                            risk_level = 'medium'
        
        return {
            'total_medications': len(medications),
            'interactions_found': len(interactions),
            'risk_level': risk_level,
            'interactions': interactions,
            'recommendations': self._get_interaction_recommendations(interactions)
        }
    
    def _get_interaction_recommendations(self, interactions: List[Dict[str, Any]]) -> List[str]:
        """Get recommendations based on drug interactions"""
        recommendations = []
        
        for interaction in interactions:
            if interaction['severity'] == 'high':
                recommendations.append(f"⚠️ High-risk interaction between {interaction['drug1']} and {interaction['drug2']}. Consider alternative therapy or close monitoring.")
            else:
                recommendations.append(f"⚡ Moderate interaction between {interaction['drug1']} and {interaction['drug2']}. Monitor for adverse effects.")
        
        if not recommendations:
            recommendations.append("✅ No significant drug interactions detected.")
        
        return recommendations

# Create global instance
medical_analytics = MedicalAnalytics()

if __name__ == "__main__":
    # Test the analytics module
    print("Testing Medical Analytics Module...")
    
    # Sample vital signs data
    sample_vitals = [
        {
            'timestamp': datetime.now() - timedelta(hours=i),
            'heart_rate': 75 + np.random.randint(-10, 10),
            'bp_systolic': 120 + np.random.randint(-15, 15),
            'bp_diastolic': 80 + np.random.randint(-10, 10),
            'temperature': 37 + np.random.uniform(-0.5, 0.5),
            'respiratory_rate': 16 + np.random.randint(-2, 2),
            'spo2': 98 + np.random.randint(-3, 0)
        }
        for i in range(24)
    ]
    
    # Analyze trends
    results = medical_analytics.analyze_vital_signs_trends(sample_vitals)
    print(f"✅ Analysis complete: {results['risk_scores']['risk_level']} risk level")
    
    # Test readmission prediction
    patient_data = {
        'age': 68,
        'gender': 'Male',
        'chronic_conditions': ['Hypertension', 'Diabetes'],
        'current_medications': ['Metformin', 'Lisinopril', 'Aspirin']
    }
    
    readmission_risk = medical_analytics.predict_readmission_risk(patient_data)
    print(f"✅ Readmission risk: {readmission_risk['risk_level']} ({readmission_risk['probability']*100:.1f}%)")
    
    print("Analytics module test complete!")
