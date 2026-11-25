import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'database', 'heart_disease.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            prediction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            input_data TEXT NOT NULL, -- JSON string of medical parameters
            prediction_status TEXT NOT NULL, -- "No Heart Disease" or "Heart Disease Detected"
            predicted_class INTEGER NOT NULL,
            probability REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def insert_prediction(patient_name, age, gender, input_data_json, prediction_status, predicted_class, probability):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO predictions (patient_name, age, gender, input_data, prediction_status, predicted_class, probability)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (patient_name, age, gender, input_data_json, prediction_status, predicted_class, probability))
    conn.commit()
    prediction_id = cursor.lastrowid
    conn.close()
    return prediction_id

def get_all_predictions():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions ORDER BY prediction_date DESC')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_prediction_by_id(prediction_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM predictions WHERE id = ?', (prediction_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None
