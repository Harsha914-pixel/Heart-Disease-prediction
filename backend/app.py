import os
import sys

from flask import Flask, send_from_directory

# Ensure the backend directory is in the path for sibling imports
_backend_dir = os.path.dirname(os.path.abspath(__file__))
_root_dir = os.path.dirname(_backend_dir)
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)
if _root_dir not in sys.path:
    sys.path.insert(0, _root_dir)

from database.database import init_db  # type: ignore[import]
from routes.prediction_routes import prediction_bp  # type: ignore[import]
from routes.history_routes import history_bp  # type: ignore[import]
from extensions import socketio  # type: ignore[import]

app = Flask(__name__, static_folder='../frontend', static_url_path='')
socketio.init_app(app)

# Register API blueprints
app.register_blueprint(prediction_bp, url_prefix='/api')
app.register_blueprint(history_bp, url_prefix='/api')

# Routes to serve frontend pages
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory(app.static_folder, 'dashboard.html')

@app.route('/prediction')
def prediction():
    return send_from_directory(app.static_folder, 'prediction.html')

@app.route('/result')
def result():
    return send_from_directory(app.static_folder, 'result.html')

@app.route('/history')
def history():
    return send_from_directory(app.static_folder, 'history.html')

@app.route('/evaluation')
def evaluation():
    return send_from_directory(app.static_folder, 'evaluation.html')

if __name__ == '__main__':
    # Initialize the SQLite database
    init_db()

    # Start the server
    print("Starting Flask-SocketIO web server...")
    print(" * Running on http://localhost:5000")
    socketio.run(app, debug=True, host='127.0.0.1', port=5000, allow_unsafe_werkzeug=True, use_reloader=False)
