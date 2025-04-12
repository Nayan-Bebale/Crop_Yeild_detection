import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import pickle
import warnings
warnings.filterwarnings('ignore')

# Load and preprocess data
def preprocess_data(df):
    df = df.dropna()
    
    # Clean categorical columns by stripping whitespace
    for col in ['Crop', 'Season', 'State']:
        df[col] = df[col].str.strip()
    
    # Define all possible seasons (add more if needed)
    all_seasons = ['Kharif', 'Rabi', 'Whole Year', 'Summer', 'Winter', 'Autumn']
    
    le_crop = LabelEncoder()
    le_season = LabelEncoder()
    le_state = LabelEncoder()
    
    # Fit encoders with all possible values
    df['Crop'] = le_crop.fit_transform(df['Crop'])
    le_season.fit(all_seasons)  # Fit with all seasons
    df['Season'] = le_season.transform(df['Season'])
    df['State'] = le_state.fit_transform(df['State'])
    
    # Save encoders
    with open('encoders.pkl', 'wb') as f:
        pickle.dump({'crop': le_crop, 'season': le_season, 'state': le_state}, f)
    
    return df

# Load data
df = pd.read_csv('data/crop_yield_data.csv')

# Preprocess data
df_processed = preprocess_data(df)

# Features and target
X = df_processed.drop('Yield', axis=1)
y = df_processed['Yield']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)

# Calculate accuracy
score = rf_model.score(X_test, y_test)
print(f"Model R² Score: {score:.4f}")

# Save the model
with open('model.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

print("Model training completed and saved as 'model.pkl'")