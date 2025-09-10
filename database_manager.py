#!/usr/bin/env python3
"""
NEXUS-MED ULTRA - Database Manager Module
Advanced medical database management system
"""

import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import pandas as pd
from contextlib import contextmanager

logger = logging.getLogger(__name__)

class MedicalDatabaseManager:
    """Advanced medical database management system"""
    
    def __init__(self, db_path: str = "medical_database.db"):
        self.db_path = db_path
        self.init_database()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize all database tables"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Patients table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS patients (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    age INTEGER,
                    gender TEXT,
                    blood_type TEXT,
                    height REAL,
                    weight REAL,
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
            
            # Medical records table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS medical_records (
                    id TEXT PRIMARY KEY,
                    patient_id TEXT NOT NULL,
                    visit_date TEXT,
                    chief_complaint TEXT,
                    symptoms TEXT,
                    vital_signs TEXT,
                    diagnosis TEXT,
                    differential_diagnosis TEXT,
                    treatment_plan TEXT,
                    prescriptions TEXT,
                    lab_results TEXT,
                    imaging_results TEXT,
                    notes TEXT,
                    follow_up TEXT,
                    provider TEXT,
                    created_at TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            ''')
            
            # Vital signs history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS vital_signs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    timestamp TEXT,
                    temperature REAL,
                    heart_rate INTEGER,
                    bp_systolic INTEGER,
                    bp_diastolic INTEGER,
                    respiratory_rate INTEGER,
                    spo2 INTEGER,
                    pain_scale INTEGER,
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            ''')
            
            # Lab results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lab_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    record_id TEXT,
                    test_name TEXT,
                    result_value TEXT,
                    unit TEXT,
                    reference_range TEXT,
                    status TEXT,
                    test_date TEXT,
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id),
                    FOREIGN KEY (record_id) REFERENCES medical_records(id)
                )
            ''')
            
            # Prescriptions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS prescriptions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    record_id TEXT,
                    medication TEXT,
                    dosage TEXT,
                    frequency TEXT,
                    duration TEXT,
                    prescriber TEXT,
                    prescribed_date TEXT,
                    start_date TEXT,
                    end_date TEXT,
                    instructions TEXT,
                    status TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id),
                    FOREIGN KEY (record_id) REFERENCES medical_records(id)
                )
            ''')
            
            # Appointments table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    appointment_date TEXT,
                    appointment_time TEXT,
                    provider TEXT,
                    department TEXT,
                    reason TEXT,
                    status TEXT,
                    notes TEXT,
                    created_at TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            ''')
            
            # Chat conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT,
                    session_id TEXT,
                    messages TEXT,
                    timestamp TEXT,
                    summary TEXT,
                    tags TEXT
                )
            ''')
            
            # Clinical notes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clinical_notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    note_type TEXT,
                    content TEXT,
                    author TEXT,
                    created_at TEXT,
                    updated_at TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            ''')
            
            # Allergies table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS allergies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    allergen TEXT,
                    reaction TEXT,
                    severity TEXT,
                    onset_date TEXT,
                    notes TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            ''')
            
            # Immunizations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS immunizations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    patient_id TEXT NOT NULL,
                    vaccine TEXT,
                    date_given TEXT,
                    dose_number INTEGER,
                    lot_number TEXT,
                    site TEXT,
                    provider TEXT,
                    next_due TEXT,
                    FOREIGN KEY (patient_id) REFERENCES patients(id)
                )
            ''')
            
            conn.commit()
            logger.info("Database initialized successfully")
    
    # Patient Management Functions
    def save_patient(self, patient_data: Dict[str, Any]) -> bool:
        """Save or update patient data"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Convert lists and dicts to JSON strings
                for field in ['allergies', 'chronic_conditions', 'current_medications', 
                             'medical_history', 'emergency_contact', 'insurance_info']:
                    if field in patient_data and isinstance(patient_data[field], (list, dict)):
                        patient_data[field] = json.dumps(patient_data[field])
                
                # Check if patient exists
                cursor.execute("SELECT id FROM patients WHERE id = ?", (patient_data['id'],))
                exists = cursor.fetchone()
                
                if exists:
                    # Update existing patient
                    patient_data['updated_at'] = datetime.now().isoformat()
                    fields = [f"{k} = ?" for k in patient_data.keys() if k != 'id']
                    values = [v for k, v in patient_data.items() if k != 'id']
                    values.append(patient_data['id'])
                    
                    cursor.execute(f"UPDATE patients SET {', '.join(fields)} WHERE id = ?", values)
                else:
                    # Insert new patient
                    fields = list(patient_data.keys())
                    placeholders = ['?' for _ in fields]
                    values = list(patient_data.values())
                    
                    cursor.execute(
                        f"INSERT INTO patients ({', '.join(fields)}) VALUES ({', '.join(placeholders)})",
                        values
                    )
                
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving patient: {e}")
            return False
    
    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        """Get patient by ID"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
                row = cursor.fetchone()
                
                if row:
                    patient = dict(row)
                    # Parse JSON fields
                    for field in ['allergies', 'chronic_conditions', 'current_medications', 
                                 'medical_history', 'emergency_contact', 'insurance_info']:
                        if field in patient and patient[field]:
                            try:
                                patient[field] = json.loads(patient[field])
                            except:
                                pass
                    return patient
                return None
        except Exception as e:
            logger.error(f"Error getting patient: {e}")
            return None
    
    def get_all_patients(self) -> List[Dict[str, Any]]:
        """Get all patients"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM patients ORDER BY name")
                rows = cursor.fetchall()
                
                patients = []
                for row in rows:
                    patient = dict(row)
                    # Parse JSON fields
                    for field in ['allergies', 'chronic_conditions', 'current_medications', 
                                 'medical_history', 'emergency_contact', 'insurance_info']:
                        if field in patient and patient[field]:
                            try:
                                patient[field] = json.loads(patient[field])
                            except:
                                pass
                    patients.append(patient)
                
                return patients
        except Exception as e:
            logger.error(f"Error getting patients: {e}")
            return []
    
    # Medical Records Functions
    def save_medical_record(self, record_data: Dict[str, Any]) -> bool:
        """Save medical record"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Convert lists and dicts to JSON
                json_fields = ['symptoms', 'vital_signs', 'diagnosis', 'differential_diagnosis',
                              'prescriptions', 'lab_results', 'imaging_results']
                for field in json_fields:
                    if field in record_data and isinstance(record_data[field], (list, dict)):
                        record_data[field] = json.dumps(record_data[field])
                
                fields = list(record_data.keys())
                placeholders = ['?' for _ in fields]
                values = list(record_data.values())
                
                cursor.execute(
                    f"INSERT INTO medical_records ({', '.join(fields)}) VALUES ({', '.join(placeholders)})",
                    values
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving medical record: {e}")
            return False
    
    def get_patient_records(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get all medical records for a patient"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM medical_records WHERE patient_id = ? ORDER BY visit_date DESC",
                    (patient_id,)
                )
                rows = cursor.fetchall()
                
                records = []
                for row in rows:
                    record = dict(row)
                    # Parse JSON fields
                    json_fields = ['symptoms', 'vital_signs', 'diagnosis', 'differential_diagnosis',
                                  'prescriptions', 'lab_results', 'imaging_results']
                    for field in json_fields:
                        if field in record and record[field]:
                            try:
                                record[field] = json.loads(record[field])
                            except:
                                pass
                    records.append(record)
                
                return records
        except Exception as e:
            logger.error(f"Error getting patient records: {e}")
            return []
    
    # Vital Signs Functions
    def save_vital_signs(self, patient_id: str, vitals: Dict[str, Any]) -> bool:
        """Save vital signs reading"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                vitals['patient_id'] = patient_id
                vitals['timestamp'] = vitals.get('timestamp', datetime.now().isoformat())
                
                fields = list(vitals.keys())
                placeholders = ['?' for _ in fields]
                values = list(vitals.values())
                
                cursor.execute(
                    f"INSERT INTO vital_signs ({', '.join(fields)}) VALUES ({', '.join(placeholders)})",
                    values
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving vital signs: {e}")
            return False
    
    def get_vital_signs_history(self, patient_id: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get vital signs history for a patient"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM vital_signs WHERE patient_id = ? ORDER BY timestamp DESC LIMIT ?",
                    (patient_id, limit)
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting vital signs history: {e}")
            return []
    
    # Lab Results Functions
    def save_lab_result(self, lab_data: Dict[str, Any]) -> bool:
        """Save lab result"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                fields = list(lab_data.keys())
                placeholders = ['?' for _ in fields]
                values = list(lab_data.values())
                
                cursor.execute(
                    f"INSERT INTO lab_results ({', '.join(fields)}) VALUES ({', '.join(placeholders)})",
                    values
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving lab result: {e}")
            return False
    
    def get_lab_results(self, patient_id: str, test_name: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get lab results for a patient"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if test_name:
                    cursor.execute(
                        "SELECT * FROM lab_results WHERE patient_id = ? AND test_name = ? ORDER BY test_date DESC",
                        (patient_id, test_name)
                    )
                else:
                    cursor.execute(
                        "SELECT * FROM lab_results WHERE patient_id = ? ORDER BY test_date DESC",
                        (patient_id,)
                    )
                
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting lab results: {e}")
            return []
    
    # Prescription Functions
    def save_prescription(self, prescription_data: Dict[str, Any]) -> bool:
        """Save prescription"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                prescription_data['prescribed_date'] = prescription_data.get(
                    'prescribed_date', datetime.now().isoformat()
                )
                prescription_data['status'] = prescription_data.get('status', 'active')
                
                fields = list(prescription_data.keys())
                placeholders = ['?' for _ in fields]
                values = list(prescription_data.values())
                
                cursor.execute(
                    f"INSERT INTO prescriptions ({', '.join(fields)}) VALUES ({', '.join(placeholders)})",
                    values
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving prescription: {e}")
            return False
    
    def get_active_prescriptions(self, patient_id: str) -> List[Dict[str, Any]]:
        """Get active prescriptions for a patient"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM prescriptions WHERE patient_id = ? AND status = 'active' ORDER BY prescribed_date DESC",
                    (patient_id,)
                )
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Error getting prescriptions: {e}")
            return []
    
    # Conversation Functions
    def save_conversation(self, conversation_data: Dict[str, Any]) -> bool:
        """Save chat conversation"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if 'messages' in conversation_data and isinstance(conversation_data['messages'], list):
                    conversation_data['messages'] = json.dumps(conversation_data['messages'])
                
                if 'tags' in conversation_data and isinstance(conversation_data['tags'], list):
                    conversation_data['tags'] = json.dumps(conversation_data['tags'])
                
                conversation_data['timestamp'] = conversation_data.get(
                    'timestamp', datetime.now().isoformat()
                )
                
                fields = list(conversation_data.keys())
                placeholders = ['?' for _ in fields]
                values = list(conversation_data.values())
                
                cursor.execute(
                    f"INSERT INTO conversations ({', '.join(fields)}) VALUES ({', '.join(placeholders)})",
                    values
                )
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
            return False
    
    def get_conversations(self, patient_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get conversations, optionally filtered by patient"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if patient_id:
                    cursor.execute(
                        "SELECT * FROM conversations WHERE patient_id = ? ORDER BY timestamp DESC",
                        (patient_id,)
                    )
                else:
                    cursor.execute("SELECT * FROM conversations ORDER BY timestamp DESC")
                
                rows = cursor.fetchall()
                conversations = []
                for row in rows:
                    conv = dict(row)
                    if 'messages' in conv and conv['messages']:
                        try:
                            conv['messages'] = json.loads(conv['messages'])
                        except:
                            pass
                    if 'tags' in conv and conv['tags']:
                        try:
                            conv['tags'] = json.loads(conv['tags'])
                        except:
                            pass
                    conversations.append(conv)
                
                return conversations
        except Exception as e:
            logger.error(f"Error getting conversations: {e}")
            return []
    
    # Analytics Functions
    def get_patient_analytics(self, patient_id: str) -> Dict[str, Any]:
        """Get comprehensive analytics for a patient"""
        try:
            analytics = {
                'patient_id': patient_id,
                'total_visits': 0,
                'total_prescriptions': 0,
                'active_prescriptions': 0,
                'total_lab_tests': 0,
                'vital_signs_count': 0,
                'last_visit': None,
                'common_diagnoses': [],
                'medication_history': []
            }
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Count visits
                cursor.execute(
                    "SELECT COUNT(*) as count FROM medical_records WHERE patient_id = ?",
                    (patient_id,)
                )
                analytics['total_visits'] = cursor.fetchone()['count']
                
                # Get last visit
                cursor.execute(
                    "SELECT visit_date FROM medical_records WHERE patient_id = ? ORDER BY visit_date DESC LIMIT 1",
                    (patient_id,)
                )
                last_visit = cursor.fetchone()
                if last_visit:
                    analytics['last_visit'] = last_visit['visit_date']
                
                # Count prescriptions
                cursor.execute(
                    "SELECT COUNT(*) as total, SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END) as active FROM prescriptions WHERE patient_id = ?",
                    (patient_id,)
                )
                rx_data = cursor.fetchone()
                analytics['total_prescriptions'] = rx_data['total']
                analytics['active_prescriptions'] = rx_data['active'] or 0
                
                # Count lab tests
                cursor.execute(
                    "SELECT COUNT(*) as count FROM lab_results WHERE patient_id = ?",
                    (patient_id,)
                )
                analytics['total_lab_tests'] = cursor.fetchone()['count']
                
                # Count vital signs
                cursor.execute(
                    "SELECT COUNT(*) as count FROM vital_signs WHERE patient_id = ?",
                    (patient_id,)
                )
                analytics['vital_signs_count'] = cursor.fetchone()['count']
                
                # Get common diagnoses
                cursor.execute(
                    "SELECT diagnosis FROM medical_records WHERE patient_id = ? AND diagnosis IS NOT NULL",
                    (patient_id,)
                )
                diagnoses = []
                for row in cursor.fetchall():
                    if row['diagnosis']:
                        try:
                            diag_list = json.loads(row['diagnosis'])
                            diagnoses.extend(diag_list)
                        except:
                            diagnoses.append(row['diagnosis'])
                
                # Count diagnosis frequency
                from collections import Counter
                diag_counts = Counter(diagnoses)
                analytics['common_diagnoses'] = [
                    {'diagnosis': diag, 'count': count} 
                    for diag, count in diag_counts.most_common(5)
                ]
                
                # Get medication history
                cursor.execute(
                    "SELECT DISTINCT medication FROM prescriptions WHERE patient_id = ? ORDER BY prescribed_date DESC LIMIT 10",
                    (patient_id,)
                )
                analytics['medication_history'] = [row['medication'] for row in cursor.fetchall()]
                
            return analytics
            
        except Exception as e:
            logger.error(f"Error getting patient analytics: {e}")
            return {}
    
    def export_patient_data(self, patient_id: str, format: str = 'json') -> Optional[Any]:
        """Export all patient data in specified format"""
        try:
            # Gather all patient data
            patient = self.get_patient(patient_id)
            if not patient:
                return None
            
            data = {
                'patient': patient,
                'medical_records': self.get_patient_records(patient_id),
                'vital_signs': self.get_vital_signs_history(patient_id),
                'lab_results': self.get_lab_results(patient_id),
                'prescriptions': self.get_active_prescriptions(patient_id),
                'analytics': self.get_patient_analytics(patient_id)
            }
            
            if format == 'json':
                return json.dumps(data, indent=2, default=str)
            elif format == 'dataframe':
                # Convert to pandas DataFrames
                dfs = {}
                for key, value in data.items():
                    if isinstance(value, list) and value:
                        dfs[key] = pd.DataFrame(value)
                    elif isinstance(value, dict):
                        dfs[key] = pd.DataFrame([value])
                return dfs
            else:
                return data
                
        except Exception as e:
            logger.error(f"Error exporting patient data: {e}")
            return None

# Create global instance
db_manager = MedicalDatabaseManager()

if __name__ == "__main__":
    # Test the database manager
    print("Testing Medical Database Manager...")
    
    # Test patient creation
    test_patient = {
        'id': 'test_001',
        'name': 'Test Patient',
        'age': 35,
        'gender': 'Male',
        'blood_type': 'O+',
        'allergies': ['Penicillin', 'Peanuts'],
        'chronic_conditions': ['Hypertension'],
        'created_at': datetime.now().isoformat()
    }
    
    if db_manager.save_patient(test_patient):
        print("✅ Patient saved successfully")
    
    # Test retrieval
    patient = db_manager.get_patient('test_001')
    if patient:
        print(f"✅ Patient retrieved: {patient['name']}")
    
    print("Database manager test complete!")
