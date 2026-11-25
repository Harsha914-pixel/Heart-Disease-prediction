from flask import Blueprint, jsonify, send_from_directory
import os

from database.database import get_all_predictions, get_prediction_by_id

history_bp = Blueprint('history_bp', __name__)
REPORTS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', 'reports')

@history_bp.route('/history', methods=['GET'])
def get_history():
    try:
        predictions = get_all_predictions()
        return jsonify(predictions)
    except Exception as e:
        print(f"Error fetching prediction history: {str(e)}")
        return jsonify({"error": "Failed to fetch prediction history"}), 500

@history_bp.route('/report/<int:prediction_id>', methods=['GET'])
def get_report(prediction_id):
    try:
        pred = get_prediction_by_id(prediction_id)
        if not pred:
            return jsonify({"error": "Report not found"}), 404
            
        pdf_filename = f"heart_disease_report_{prediction_id}.pdf"
        pdf_path = os.path.join(REPORTS_DIR, pdf_filename)
        
        if os.path.exists(pdf_path):
            return send_from_directory(REPORTS_DIR, pdf_filename, as_attachment=True)
        else:
            return jsonify({"error": "PDF file does not exist"}), 404
    except Exception as e:
        print(f"Error retrieving report: {str(e)}")
        return jsonify({"error": "Failed to retrieve report"}), 500
