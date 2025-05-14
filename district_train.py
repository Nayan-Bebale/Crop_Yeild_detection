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
    # Replace -1 or invalid values with NaN
    df = df.replace(-1, np.nan)
    
    # Drop rows with missing critical columns
    df = df.dropna(subset=['State Name', 'Dist Name', 'Year'])
    
    # Define crops and their seasons
    crop_columns = [
        ('RICE', 'Kharif'),
        ('WHEAT', 'Rabi'),
        ('KHARIF SORGHUM', 'Kharif'),
        ('RABI SORGHUM', 'Rabi'),
        ('PEARL MILLET', 'Kharif'),
        ('MAIZE', 'Kharif'),
        ('CHICKPEA', 'Rabi'),
        ('PIGEONPEA', 'Kharif'),
        ('GROUNDNUT', 'Kharif')
    ]
    
    data = []
    for crop, season in crop_columns:
        # Select relevant columns
        crop_data = df[[
            'Dist Name', 'State Name', 'Year',
            f'{crop} AREA (1000 ha)', f'{crop} PRODUCTION (1000 tons)', f'{crop} YIELD (Kg per ha)'
        ]].copy()
        
        # Rename columns for consistency
        crop_data = crop_data.rename(columns={
            f'{crop} AREA (1000 ha)': 'Area',
            f'{crop} PRODUCTION (1000 tons)': 'Production',
            f'{crop} YIELD (Kg per ha)': 'Yield'
        })
        
        # Filter valid data (Area > 0, non-negative Production and Yield)
        crop_data = crop_data[crop_data['Area'] > 0]
        crop_data = crop_data[crop_data['Production'].notna() & (crop_data['Production'] >= 0)]
        crop_data = crop_data[crop_data['Yield'].notna() & (crop_data['Yield'] >= 0)]
        
        # Add Crop and Season columns
        crop_name = crop.replace('KHARIF ', '').replace('RABI ', '')  # Normalize crop name
        crop_data['Crop'] = crop_name
        crop_data['Season'] = season
        
        data.append(crop_data)
    
    # Concatenate all crop data
    df_processed = pd.concat(data, ignore_index=True)
    
    # Clean categorical columns
    df_processed['State Name'] = df_processed['State Name'].str.strip()
    df_processed['Dist Name'] = df_processed['Dist Name'].str.strip()
    
    # Encode categorical variables
    le_crop = LabelEncoder()
    le_season = LabelEncoder()
    le_state = LabelEncoder()
    le_district = LabelEncoder()
    
    # Fit season encoder with only relevant seasons
    le_season.fit(['Kharif', 'Rabi'])
    
    df_processed['Crop'] = le_crop.fit_transform(df_processed['Crop'])
    df_processed['Season'] = le_season.transform(df_processed['Season'])
    df_processed['State Name'] = le_state.fit_transform(df_processed['State Name'])
    df_processed['Dist Name'] = le_district.fit_transform(df_processed['Dist Name'])
    
    # Save encoders
    with open('encoders_district.pkl', 'wb') as f:
        pickle.dump({
            'crop': le_crop,
            'season': le_season,
            'state': le_state,
            'district': le_district
        }, f)
    
    return df_processed

# Load data
df = pd.read_csv('data\ICRISAT-District Level Data.csv')

# Preprocess data
df_processed = preprocess_data(df)

# Features and target
X = df_processed[['Crop', 'Year', 'Season', 'State Name', 'Dist Name', 'Area', 'Production']]
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
with open('model_district.pkl', 'wb') as f:
    pickle.dump(rf_model, f)

print("Model training completed and saved as 'model.pkl'")