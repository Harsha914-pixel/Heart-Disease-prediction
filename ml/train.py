import os
import json
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC

from preprocessing import get_preprocessing_pipeline

def train_and_evaluate():
    # 1. Load dataset
    csv_path = 'ml/dataset/heart_disease.csv'
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"Dataset not found at {csv_path}. Please download it first.")
        
    df = pd.read_csv(csv_path)
    
    # Clean rows where target 'num' is missing
    df = df.dropna(subset=['num'])
    
    # Separate features and target
    X = df.drop(columns=['num'])
    y = df['num']
    
    # 2. Split into train and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 3. Create and fit preprocessing pipeline
    preprocessor = get_preprocessing_pipeline()
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Save the fitted preprocessing pipeline
    os.makedirs('ml/trained_model', exist_ok=True)
    joblib.dump(preprocessor, 'ml/trained_model/preprocessing_pipeline.pkl')
    print("Saved preprocessing pipeline to ml/trained_model/preprocessing_pipeline.pkl")
    
    # 4. Initialize models
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Decision Tree': DecisionTreeClassifier(random_state=42),
        'Random Forest': RandomForestClassifier(random_state=42, n_estimators=100),
        'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
        'Support Vector Machine': SVC(probability=True, random_state=42)
    }
    
    results = {}
    best_acc = 0.0
    best_model_name = None
    best_model = None
    
    # 5. Train and evaluate each model
    for name, model in models.items():
        # Train
        model.fit(X_train_processed, y_train)
        
        # Predict
        y_pred = model.predict(X_test_processed)
        
        # Calculate metrics (weighted average since multiclass)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y_test, y_pred, average='weighted', zero_division=0)
        f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
        
        cm = confusion_matrix(y_test, y_pred).tolist()
        
        results[name] = {
            'accuracy': float(acc),
            'precision': float(prec),
            'recall': float(rec),
            'f1_score': float(f1),
            'confusion_matrix': cm
        }
        
        print(f"Model: {name}")
        print(f"  Accuracy:  {acc:.4f}")
        print(f"  Precision: {prec:.4f}")
        print(f"  Recall:    {rec:.4f}")
        print(f"  F1 Score:  {f1:.4f}")
        print("-" * 30)
        
        # Select best model based on accuracy (and F1 if tied)
        if acc > best_acc:
            best_acc = acc
            best_model_name = name
            best_model = model
            
    # Save evaluation summary
    eval_summary = {
        'dataset_size': len(df),
        'training_samples': len(X_train),
        'testing_samples': len(X_test),
        'selected_algorithm': best_model_name,
        'model_performances': results
    }
    
    with open('ml/trained_model/evaluation_results.json', 'w') as f:
        json.dump(eval_summary, f, indent=4)
    print(f"Saved evaluation results to ml/trained_model/evaluation_results.json")
    
    # Save the best model
    joblib.dump(best_model, 'ml/trained_model/heart_disease_model.pkl')
    print(f"Saved best model ({best_model_name}) to ml/trained_model/heart_disease_model.pkl")

if __name__ == '__main__':
    train_and_evaluate()
