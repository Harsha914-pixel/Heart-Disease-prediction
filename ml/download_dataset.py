import os
import pandas as pd
from ucimlrepo import fetch_ucirepo

def download_data():
    print("Fetching Cleveland Heart Disease dataset...")
    # Fetch dataset (id 45 is Heart Disease)
    heart_disease = fetch_ucirepo(id=45)
    
    # Get features and targets
    X = heart_disease.data.features
    y = heart_disease.data.targets
    
    # Combine into a single DataFrame
    df = pd.concat([X, y], axis=1)
    
    # Create directory if not exists
    os.makedirs('ml/dataset', exist_ok=True)
    
    # Save to CSV
    csv_path = 'ml/dataset/heart_disease.csv'
    df.to_csv(csv_path, index=False)
    print(f"Dataset successfully saved to {csv_path}")
    print("Columns:", list(df.columns))
    print("Shape:", df.shape)

if __name__ == '__main__':
    download_data()
