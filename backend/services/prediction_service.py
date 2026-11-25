import os
import joblib
import pandas as pd
import numpy as np

# Absolute paths to saved artifacts
PREPROCESSOR_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'trained_model', 'preprocessing_pipeline.pkl')
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'ml', 'trained_model', 'heart_disease_model.pkl')

class PredictionService:
    def __init__(self):
        self.preprocessor = None
        self.model = None
        self.load_artifacts()

    def load_artifacts(self):
        if os.path.exists(PREPROCESSOR_PATH) and os.path.exists(MODEL_PATH):
            self.preprocessor = joblib.load(PREPROCESSOR_PATH)
            self.model = joblib.load(MODEL_PATH)
        else:
            print("Warning: ML model artifacts not found. Please train the model first.")

    def predict(self, input_data):
        if self.model is None or self.preprocessor is None:
            raise RuntimeError("Model or preprocessing pipeline is not loaded.")
        
        # Convert single input dict to DataFrame with expected columns
        # Features: age, sex, cp, trestbps, chol, fbs, restecg, thalach, exang, oldpeak, slope, ca, thal
        feature_order = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']
        
        input_dict = {k: [input_data[k]] for k in feature_order}
        df_input = pd.DataFrame(input_dict)
        
        # Preprocess features
        processed_features = self.preprocessor.transform(df_input)
        
        # Predict class
        predicted_class = int(self.model.predict(processed_features)[0])
        
        # Get probability/confidence
        probability = None
        if hasattr(self.model, 'predict_proba'):
            prob_array = self.model.predict_proba(processed_features)[0]
            # Since multiclass, we can return the probability of the predicted class or
            # the probability of the presence of heart disease (sum of prob(1) + prob(2) + prob(3) + prob(4))
            # Let's return the probability of the predicted class.
            probability = float(prob_array[predicted_class])
        
        status = "No Heart Disease" if predicted_class == 0 else "Heart Disease Detected"
        
        return {
            "prediction": status,
            "class": predicted_class,
            "probability": probability
        }
