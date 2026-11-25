import os
import sys
import json
import pytest

# Add paths to sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from backend.services.prediction_service import PredictionService
from backend.services.report_service import generate_pdf_report
from backend.database.database import init_db, insert_prediction, get_prediction_by_id
from backend.app import app

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_db()

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_prediction_service_loading():
    service = PredictionService()
    assert service.model is not None
    assert service.preprocessor is not None

def test_prediction_inference():
    service = PredictionService()
    # Dummy patient inputs
    patient_data = {
        'age': 55,
        'sex': 1,
        'cp': 4,
        'trestbps': 140.0,
        'chol': 250.0,
        'fbs': 0,
        'restecg': 1,
        'thalach': 150.0,
        'exang': 0,
        'oldpeak': 1.5,
        'slope': 2,
        'ca': 0,
        'thal': 3
    }
    res = service.predict(patient_data)
    assert 'prediction' in res
    assert 'class' in res
    assert 'probability' in res
    assert res['class'] in [0, 1, 2, 3, 4]

def test_report_generation():
    input_data = {
        'trestbps': 120, 'chol': 200, 'cp': 1, 'fbs': 0,
        'restecg': 0, 'thalach': 160, 'exang': 0, 'oldpeak': 0.0,
        'slope': 1, 'ca': 0, 'thal': 3
    }
    pdf_filename = generate_pdf_report(
        prediction_id=9999,
        patient_name="Test Patient",
        age=30,
        gender="Male",
        input_data_json=json.dumps(input_data),
        prediction_status="No Heart Disease",
        predicted_class=0,
        probability=0.95
    )
    
    pdf_path = os.path.join(os.path.dirname(__file__), '../reports', pdf_filename)
    assert os.path.exists(pdf_path)
    # Clean up
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

def test_api_predict_and_history(client):
    payload = {
        'patient_name': "Alice Test",
        'age': 45,
        'gender': "Female",
        'cp': 2,
        'trestbps': 130,
        'chol': 220,
        'fbs': 0,
        'restecg': 1,
        'thalach': 155,
        'exang': 0,
        'oldpeak': 0.8,
        'slope': 1,
        'ca': 0,
        'thal': 3
    }
    
    # Test POST /api/predict
    response = client.post('/api/predict', json=payload)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'id' in data
    assert 'prediction' in data
    assert 'class' in data
    
    # Test GET /api/history
    history_resp = client.get('/api/history')
    assert history_resp.status_code == 200
    history_data = json.loads(history_resp.data)
    assert len(history_data) > 0
    assert history_data[0]['patient_name'] == "Alice Test"
