# Heart Disease Prediction Using Machine Learning

An educational, professional-grade clinical screening and prediction platform using the UCI Cleveland Heart Disease dataset.

## 1. Project Overview
This project presents an interactive web application that takes a patient's medical parameters (such as age, gender, blood pressure, cholesterol, resting ECG, max heart rate, etc.) and processes them through a pre-trained Machine Learning classification model to predict the presence and severity class of heart disease.

---

## 2. Features
- **Responsive Dashboard:** View active models, assessment logs, and quick action cards.
- **Demographic & Clinical Form:** Robust form verification prevents incorrect parameters from reaching the model.
- **Multiclass Risk Analysis:** Output classification values indicating disease absence (Class 0) or specific disease severity classes (Classes 1-4).
- **Auto-generated PDF Reports:** Generates professional clinical reports with parameters, predictions, and disclaimers.
- **SQLite History:** Track patient screening histories.
- **Light/Dark Mode:** Seamless modern UI rendering.

---

## 3. Technology Stack
- **Machine Learning:** Python, Pandas, NumPy, Scikit-learn, Joblib, ucimlrepo
- **Backend API:** Python, Flask, SQLite3
- **Frontend UI:** HTML5, CSS3 (CSS Variables for dark mode), Vanilla JS, Bootstrap CDN, FontAwesome
- **PDF Engine:** ReportLab

---

## 4. Dataset Information
The system uses the **UCI Cleveland Heart Disease dataset**, containing 303 samples and 14 features:
1. `age`: Patient age
2. `sex`: Gender (1 = Male, 0 = Female)
3. `cp`: Chest pain type (1 = typical angina, 2 = atypical angina, 3 = non-anginal pain, 4 = asymptomatic)
4. `trestbps`: Resting blood pressure (in mm Hg)
5. `chol`: Serum cholesterol (mg/dl)
6. `fbs`: Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)
7. `restecg`: Resting electrocardiographic results (0, 1, 2)
8. `thalach`: Maximum heart rate achieved
9. `exang`: Exercise-induced angina (1 = yes; 0 = no)
10. `oldpeak`: ST depression induced by exercise relative to rest
11. `slope`: Peak exercise ST segment slope (1 = upsloping, 2 = flat, 3 = downsloping)
12. `ca`: Number of major vessels colored by fluoroscopy (0-3)
13. `thal`: Thalassemia (3 = normal; 6 = fixed defect; 7 = reversable defect)
14. `num`: Target severity classification (0 = absence, 1-4 = presence/severity classes)

---

## 5. Machine Learning Methodology & Evaluation
- **Preprocessing:** Categorical parameters are handled using `OneHotEncoder` and missing columns are filled using median/mode imputers. Numeric features are standardized using `StandardScaler`.
- **Model Comparison Table:**
  | Model | Accuracy | Precision | Recall | F1 Score |
  | --- | --- | --- | --- | --- |
  | **Logistic Regression (Active)** | **65.57%** | **56.40%** | **65.57%** | **60.30%** |
  | Decision Tree | 52.46% | 49.97% | 52.46% | 51.00% |
  | Random Forest | 57.38% | 51.35% | 57.38% | 54.05% |
  | K-Nearest Neighbors | 55.74% | 45.41% | 55.74% | 50.03% |
  | Support Vector Machine | 55.74% | 42.62% | 55.74% | 48.24% |

---

## 6. Project Architecture
```
Heart-Disease-Prediction/
├── frontend/
│   ├── index.html
│   ├── dashboard.html
│   ├── prediction.html
│   ├── result.html
│   ├── history.html
│   ├── evaluation.html
│   ├── css/
│   │   └── style.css
│   └── js/
│       ├── theme.js
│       ├── dashboard.js
│       ├── prediction.js
│       ├── result.js
│       └── history.js
│
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── prediction_routes.py
│   │   └── history_routes.py
│   ├── services/
│   │   ├── prediction_service.py
│   │   └── report_service.py
│   └── database/
│       └── database.py
│
├── ml/
│   ├── dataset/
│   │   └── heart_disease.csv
│   ├── preprocessing.py
│   ├── train.py
│   ├── download_dataset.py
│   └── trained_model/
│       ├── heart_disease_model.pkl
│       ├── preprocessing_pipeline.pkl
│       └── evaluation_results.json
│
├── reports/
├── database/
│   └── heart_disease.db
├── requirements.txt
└── README.md
```

---

## 7. Installation & Running Instructions

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Download Dataset and Train Model
```bash
python ml/download_dataset.py
python ml/train.py
```

### Step 3: Run Flask Server
```bash
python backend/app.py
```
Open a browser and navigate to `http://localhost:5000`.

---

## 8. API Documentation

### POST `/api/predict`
Takes patient variables and returns the model output.
**Request Body:**
```json
{
  "patient_name": "John Doe",
  "age": 45,
  "gender": "Male",
  "cp": 2,
  "trestbps": 130,
  "chol": 220,
  "fbs": 0,
  "restecg": 1,
  "thalach": 150,
  "exang": 0,
  "oldpeak": 1.2,
  "slope": 1,
  "ca": 0,
  "thal": 3
}
```
**Response Body:**
```json
{
  "id": 1,
  "prediction": "Heart Disease Detected",
  "class": 2,
  "probability": 0.655,
  "pdf_report": "heart_disease_report_1.pdf"
}
```

### GET `/api/history`
Returns all logged patient screenings from SQLite database.

### GET `/api/report/<id>`
Downloads the autogenerated PDF report matching the database prediction ID.

---

## 9. Limitations & Disclaimer
- **Limitation:** Accuracy scores reflect overall multiclass stratification. Multiclass predictions (Classes 0-4) are inherently more complex than binary targets.
- **Medical Disclaimer:** This system is built for screening/educational purposes only and should not be used as a replacement for professional clinical diagnosis.
