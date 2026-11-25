import json
from flask import Blueprint, request, jsonify, send_from_directory
import os

from services.prediction_service import PredictionService
from services.report_service import generate_pdf_report
from database.database import insert_prediction, get_prediction_by_id, get_all_predictions

prediction_bp = Blueprint('prediction_bp', __name__)
prediction_service = PredictionService()

from extensions import socketio

@prediction_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No input data provided"}), 400
            
        # Basic validation
        required_fields = ['patient_name', 'age', 'gender', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
                
        # Prepare ML inputs (cast to float/int appropriately)
        try:
            ml_input = {
                'age': int(data['age']),
                'sex': 1 if data['gender'].lower() == 'male' else 0,
                'cp': int(data['cp']),
                'trestbps': float(data['trestbps']),
                'chol': float(data['chol']),
                'fbs': int(data['fbs']),
                'restecg': int(data['restecg']),
                'thalach': float(data['thalach']),
                'exang': int(data['exang']),
                'oldpeak': float(data['oldpeak']),
                'slope': int(data['slope']),
                'ca': int(data['ca']),
                'thal': int(data['thal'])
            }
        except ValueError as ve:
            return jsonify({"error": f"Invalid numeric input: {str(ve)}"}), 400

        # Run ML model prediction
        res = prediction_service.predict(ml_input)
        
        # Save to database
        # Save features as JSON string
        input_data_json = json.dumps(ml_input)
        prediction_id = insert_prediction(
            patient_name=data['patient_name'],
            age=ml_input['age'],
            gender=data['gender'],
            input_data_json=input_data_json,
            prediction_status=res['prediction'],
            predicted_class=res['class'],
            probability=res['probability']
        )
        
        # Generate PDF report
        pdf_name = generate_pdf_report(
            prediction_id=prediction_id,
            patient_name=data['patient_name'],
            age=ml_input['age'],
            gender=data['gender'],
            input_data_json=input_data_json,
            prediction_status=res['prediction'],
            predicted_class=res['class'],
            probability=res['probability']
        )
        
        # Emit real-time event to all connected clients
        socketio.emit('new_prediction', {})
        
        return jsonify({
            "id": prediction_id,
            "prediction": res['prediction'],
            "class": res['class'],
            "probability": res['probability'],
            "pdf_report": pdf_name
        })

    except Exception as e:
        # Don't expose tracebacks to users, just log and return simple message
        print(f"Error in prediction endpoint: {str(e)}")
        return jsonify({"error": "An internal error occurred during prediction processing"}), 500

@prediction_bp.route('/evaluation', methods=['GET'])
def get_evaluation():
    eval_path = os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'trained_model', 'evaluation_results.json')
    if os.path.exists(eval_path):
        with open(eval_path, 'r') as f:
            eval_data = json.load(f)
        return jsonify(eval_data)
    else:
        return jsonify({"error": "Evaluation metrics not available"}), 404
