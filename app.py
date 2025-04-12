from flask import Flask, render_template, request
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load model and encoders with error handling
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
except Exception as e:
    print(f"Error loading model or encoders: {e}")
    model = None
    encoders = None

# State coordinates
state_coords = {
    'Andaman and Nicobar Islands': [11.7401, 92.6586],
    'Andhra Pradesh': [15.9129, 79.7400],
    'Arunachal Pradesh': [28.2180, 94.7278],
    'Assam': [26.2006, 92.9376],
    'Bihar': [25.0961, 85.3131],
    'Chandigarh': [30.7333, 76.7794],
    'Chhattisgarh': [21.2787, 81.8661],
    'Dadra and Nagar Haveli': [20.1809, 73.0169],
    'Goa': [15.2993, 74.1240],
    'Gujarat': [22.2587, 71.1924],
    'Haryana': [29.0588, 76.0856],
    'Himachal Pradesh': [31.1048, 77.1734],
    'Jammu and Kashmir': [33.7782, 76.5762],
    'Jharkhand': [23.6102, 85.2799],
    'Karnataka': [15.3173, 75.7139],
    'Kerala': [10.8505, 76.2711],
    'Madhya Pradesh': [22.9734, 78.6569],
    'Maharashtra': [19.7515, 75.7139],
    'Manipur': [24.6637, 93.9063],
    'Meghalaya': [25.4670, 91.3662],
    'Mizoram': [23.1645, 92.9376],
    'Nagaland': [26.1584, 94.5624],
    'Odisha': [20.9517, 85.0985],
    'Puducherry': [11.9416, 79.8083],
    'Punjab': [31.1471, 75.3412],
    'Rajasthan': [27.0238, 74.2179],
    'Sikkim': [27.5330, 88.5122],
    'Tamil Nadu': [11.1271, 78.6569],
    'Telangana': [17.1232, 79.2089],
    'Tripura': [23.9408, 91.9882],
    'Uttar Pradesh': [26.8467, 80.9462],
    'Uttarakhand': [30.0668, 79.0193],
    'West Bengal': [22.9868, 87.8550]
}

@app.route('/')
def home():
    if model is None or encoders is None:
        return "Error: Model or encoders not loaded properly. Please check the server logs."
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or encoders is None:
        return "Error: Model or encoders not loaded properly."
    
    try:
        # Get form data
        input_data = {
            'Crop': request.form['crop'].strip(),
            'Crop_Year': float(request.form['year']),
            'Season': request.form['season'].strip(),  # Remove leading/trailing spaces
            'State': request.form['state'].strip(),
            'Area': float(request.form['area']),
            'Production': float(request.form['production']),
            'Annual_Rainfall': float(request.form['rainfall']),
            'Fertilizer': float(request.form['fertilizer']),
            'Pesticide': float(request.form['pesticide'])
        }
        
        # Encode categorical variables with error handling
        df = pd.DataFrame([input_data])
        
        # Check if values exist in encoder classes
        for col, encoder in [('Crop', encoders['crop']), ('Season', encoders['season']), ('State', encoders['state'])]:
            input_value = input_data[col]
            if input_value not in encoder.classes_:
                return f"Error: '{input_value}' is not a recognized {col}. Please use a value from the training data."
            df[col] = encoder.transform(df[col])
        
        # Make prediction
        prediction = model.predict(df)[0]
        
        # Get coordinates for map
        coords = state_coords.get(input_data['State'], [20.5937, 78.9629])  # Default to India center
        
        return render_template('result.html', 
                            prediction=prediction,
                            state=input_data['State'],
                            lat=coords[0],
                            lon=coords[1],
                            input_data=input_data)
    except Exception as e:
        return f"Error during prediction: {e}"
    

@app.route('/trends', methods=['GET', 'POST'])
def trends():
    if request.method == 'POST':
        crop = request.form['crop'].strip()
        state = request.form['state'].strip()
        
        df = pd.read_csv('data/crop_yield_data.csv')
        df['Crop'] = df['Crop'].str.strip()
        df['State'] = df['State'].str.strip()
        
        trend_data = df[(df['Crop'] == crop) & (df['State'] == state)][['Crop_Year', 'Yield']]
        trend_data = trend_data.groupby('Crop_Year').mean().reset_index()
        
        years = trend_data['Crop_Year'].tolist()
        yields = trend_data['Yield'].tolist()
        
        return render_template('trends.html', crop=crop, state=state, years=years, yields=yields)
    return render_template('trends.html')



@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    if request.method == 'POST':
        state = request.form['state'].strip()
        season = request.form['season'].strip()
        
        df = pd.read_csv('data/crop_yield_data.csv')
        df['State'] = df['State'].str.strip()
        df['Season'] = df['Season'].str.strip()
        
        filtered_df = df[(df['State'] == state) & (df['Season'] == season)]
        recommendations = filtered_df.groupby('Crop')['Yield'].mean().sort_values(ascending=False).head(3).to_dict()
        
        return render_template('recommend.html', state=state, season=season, recommendations=recommendations)
    return render_template('recommend.html')


if __name__ == '__main__':
    app.run(debug=True)