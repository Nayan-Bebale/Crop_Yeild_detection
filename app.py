import traceback
from flask import Flask, render_template, request, send_file
import pickle
import pandas as pd
import numpy as np
import pickle
from india import state_coords
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# Load district coordinates once when the app starts
csv_path = os.path.join('data', 'Ind_adm2_Points.csv')
df_district = pd.read_csv(csv_path)
# Normalize district names: remove extra spaces and use title case (e.g., "Andaman Islands")
df_district['District'] = df_district['District'].str.strip().str.title()
# Group by district and take the first coordinate to handle duplicates
district_coords = df_district.groupby('District').first()[['Latitude', 'Longitude']]

# Load model and encoders with error handling
try:
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    with open('encoders.pkl', 'rb') as f:
        encoders = pickle.load(f)
    with open('model_district.pkl', 'rb') as f:
        model_district = pickle.load(f)
    with open('encoders_district.pkl', 'rb') as f:
        encoders_district = pickle.load(f)
except Exception as e:
    print(f"Error loading model or encoders: {e}")
    model = None
    encoders = None


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


################################################################## District Prediction ##################################################################


@app.route('/dist_prediction')
def dist_prediction():
    return render_template('dist_index.html')


@app.route('/dist_predict', methods=['POST'])
def dist_predict():
    try:
        # Get input data from form
        input_data = {
            'Crop': request.form['crop'].strip().upper(),
            'Year': float(request.form['year']),
            'Season': request.form['season'].strip(),
            'State Name': request.form['state'].strip(),
            'Dist Name': request.form['district'].strip().title(),  # Normalize to title case
            'Area': float(request.form['area']),
            'Production': float(request.form['production'])
        }

        # Validate inputs (assuming encoders_district is defined elsewhere)
        if input_data['Crop'] not in encoders_district['crop'].classes_:
            raise ValueError(f"Invalid crop name: {input_data['Crop']}.")
        if input_data['Season'] not in encoders_district['season'].classes_:
            raise ValueError(f"Invalid season: {input_data['Season']}.")
        if input_data['State Name'] not in encoders_district['state'].classes_:
            raise ValueError(f"Invalid state: {input_data['State Name']}.")
        if input_data['Dist Name'] not in encoders_district['district'].classes_:
            raise ValueError(f"Invalid district: {input_data['Dist Name']}.")

        # Create DataFrame
        input_df = pd.DataFrame([input_data])

        # Encode categorical fields (assuming encoders_district is defined)
        input_df['Crop'] = encoders_district['crop'].transform(input_df['Crop'])
        input_df['Season'] = encoders_district['season'].transform(input_df['Season'])
        input_df['State Name'] = encoders_district['state'].transform(input_df['State Name'])
        input_df['Dist Name'] = encoders_district['district'].transform(input_df['Dist Name'])

        # Predict (assuming model_district is defined)
        prediction = model_district.predict(input_df)[0]

        # Get coordinates
        if input_data['Dist Name'] in district_coords.index:
            coords = district_coords.loc[input_data['Dist Name']]
            lat = coords['Latitude']
            lon = coords['Longitude']
        else:
            raise ValueError(f"Coordinates not found for district: {input_data['Dist Name']}")

        # Render the result page
        return render_template('dist_result.html',
                               prediction=prediction,
                               district=input_data['Dist Name'],
                               state=input_data['State Name'],
                               lat=lat,
                               lon=lon,
                               input_data=input_data)

    except ValueError as ve:
        return render_template('error.html', error=str(ve))
    except Exception as e:
        error_message = f"An unexpected error occurred: {str(e)}\n{traceback.format_exc()}"
        return render_template('error.html', error=error_message)



@app.route('/dist_trends', methods=['GET', 'POST'])
def dist_trends():
    if request.method == 'POST':
        district = request.form['district'].strip()
        crops = request.form.getlist('crops')  # Multiple crops
        
        df = pd.read_csv('data/ICRISAT-District Level Data.csv')
        df['Dist Name'] = df['Dist Name'].str.strip()
        
        trend_data = []
        for crop in crops:
            yield_col = f'{crop} YIELD (Kg per ha)'
            if yield_col in df.columns:
                crop_data = df[df['Dist Name'] == district][['Year', yield_col]]
                crop_data = crop_data.groupby('Year').mean().reset_index()
                crop_data = crop_data[crop_data[yield_col] > 0]
                trend_data.append({
                    'crop': crop,
                    'years': crop_data['Year'].tolist(),
                    'yields': crop_data[yield_col].tolist()
                })
        
        return render_template('dist_trends.html', district=district, trend_data=trend_data)
    return render_template('dist_trends.html')


@app.route('/dist_compare', methods=['GET', 'POST'])
def dist_compare():
    if request.method == 'POST':
        try:
            district = request.form['district'].strip()
            year = int(request.form['year'])
            
            # Load dataset
            df = pd.read_csv('data/ICRISAT-District Level Data.csv')
            df['Dist Name'] = df['Dist Name'].str.strip()
            
            # Validate inputs
            if district not in df['Dist Name'].values:
                return render_template('dist_compare.html', error=f"District '{district}' not found in the dataset.")
            if year not in df['Year'].values:
                return render_template('dist_compare.html', error=f"Year {year} not found in the dataset.")
            
            # Define crops (include Kharif/Rabi for SORGHUM)
            crops = ['RICE', 'WHEAT', 'KHARIF SORGHUM', 'RABI SORGHUM', 'PEARL MILLET', 'MAIZE', 'CHICKPEA', 'PIGEONPEA', 'GROUNDNUT']
            comparison = []
            for crop in crops:
                yield_col = f'{crop} YIELD (Kg per ha)'
                if yield_col in df.columns:
                    data = df[(df['Dist Name'] == district) & (df['Year'] == year)][yield_col]
                    if not data.empty and data.iloc[0] > 0 and pd.notna(data.iloc[0]):
                        comparison.append({'crop': crop, 'yield': float(data.iloc[0])})
            
            # Extract crop names and yields for Chart.js
            crop_names = [item['crop'] for item in comparison]
            crop_yields = [item['yield'] for item in comparison]
            
            if not comparison:
                return render_template('dist_compare.html', 
                                     district=district, 
                                     year=year, 
                                     error="No valid crop yield data found for this district and year.")
            
            return render_template('dist_compare.html', 
                                 district=district, 
                                 year=year, 
                                 comparison=comparison,
                                 crop_names=crop_names,
                                 crop_yields=crop_yields)
        except FileNotFoundError:
            return render_template('dist_compare.html', error="Dataset file not found. Please check the file path.")
        except ValueError as ve:
            return render_template('dist_compare.html', error="Invalid input: Please enter a valid year.")
        except Exception as e:
            return render_template('dist_compare.html', error=f"An error occurred: {str(e)}")
    
    return render_template('dist_compare.html')

   


@app.route('/dist_insights', methods=['GET', 'POST'])
def dist_insights():
    # Initialize default variables
    error = None
    top_districts = []
    avg_yields = {}
    hist_data = []
    bin_edges = []
    production_shares = {}
    scatter_data = []
    years = []
    crops = ['RICE', 'WHEAT', 'KHARIF SORGHUM', 'RABI SORGHUM', 'PEARL MILLET', 'MAIZE', 'CHICKPEA', 'PIGEONPEA', 'GROUNDNUT']
    selected_year = None
    selected_crop = 'RICE'

    try:
        # Load dataset
        df = pd.read_csv('data/ICRISAT-District Level Data.csv')
        df['Dist Name'] = df['Dist Name'].str.strip()
        
        # Get available years
        years = sorted(df['Year'].unique())
        if not years:
            raise ValueError("No valid years found in the dataset.")
        
        # Default or selected year and crop
        selected_year = int(request.form.get('year', years[-1])) if request.method == 'POST' else years[-1]
        selected_crop = request.form.get('crop', 'RICE') if request.method == 'POST' else 'RICE'
        
        # Validate selected crop
        if selected_crop not in crops:
            raise ValueError(f"Invalid crop selected: {selected_crop}")

        # 1. Top-performing districts by crop (for table)
        for crop in crops:
            yield_col = f'{crop} YIELD (Kg per ha)'
            if yield_col in df.columns:
                avg_yield = df[df[yield_col] > 0].groupby('Dist Name')[yield_col].mean().sort_values(ascending=False)
                if not avg_yield.empty:
                    top_districts.append({
                        'district': avg_yield.index[0],
                        'crop': crop,
                        'yield': round(avg_yield.iloc[0], 2)
                    })
        
        # 2. Average yield per crop (for bar chart)
        for crop in crops:
            yield_col = f'{crop} YIELD (Kg per ha)'
            if yield_col in df.columns:
                avg_yield = df[df[yield_col] > 0][yield_col].mean()
                if pd.notna(avg_yield):
                    avg_yields[crop] = round(avg_yield, 2)
        
        # 3. Yield distribution for selected crop (for histogram)
        yield_col = f'{selected_crop} YIELD (Kg per ha)'
        if yield_col in df.columns:
            yields = df[df[yield_col] > 0][yield_col].dropna().values
            if yields.size > 0:
                hist_data, bin_edges = np.histogram(yields, bins=10, range=(0, max(yields)))
                hist_data = hist_data.tolist()
                bin_edges = [round(edge, 2) for edge in bin_edges]
        
        # 4. Production share by crop for selected year (for pie chart)
        total_production = 0
        for crop in crops:
            prod_col = f'{crop} PRODUCTION (1000 tons)'
            if prod_col in df.columns:
                prod = df[(df['Year'] == selected_year) & (df[prod_col] > 0)][prod_col].sum()
                if pd.notna(prod):
                    production_shares[crop] = round(prod, 2)
                    total_production += prod
        # Convert to percentages
        if total_production > 0:
            production_shares = {crop: round((prod / total_production * 100), 2) for crop, prod in production_shares.items()}
        else:
            production_shares = {}
        
        # 5. Scatter plot data for selected crop (Area vs. Yield, sized by Production)
        area_col = f'{selected_crop} AREA (1000 ha)'
        prod_col = f'{selected_crop} PRODUCTION (1000 tons)'
        if yield_col in df.columns and area_col in df.columns and prod_col in df.columns:
            data = df[(df[yield_col] > 0) & (df[area_col] > 0) & (df[prod_col] > 0)][['Dist Name', area_col, yield_col, prod_col]]
            for _, row in data.iterrows():
                scatter_data.append({
                    'district': row['Dist Name'],
                    'area': round(row[area_col], 2),
                    'yield': round(row[yield_col], 2),
                    'production': round(row[prod_col], 2)
                })
        
    except FileNotFoundError:
        error = "Dataset file not found. Please check the file path."
    except Exception as e:
        error = f"An error occurred: {str(e)}"

    # Always render the template with all variables
    return render_template('insights.html',
                         top_districts=top_districts,
                         avg_yields=avg_yields,
                         hist_data=hist_data,
                         bin_edges=bin_edges,
                         production_shares=production_shares,
                         scatter_data=scatter_data,
                         years=years,
                         crops=crops,
                         selected_year=selected_year,
                         selected_crop=selected_crop,
                         error=error)




@app.route('/download', methods=['POST'])
def download():
    input_data = request.form.to_dict()
    prediction = float(request.form.get('prediction', 0))
    
    filename = "district_report.pdf"
    c = canvas.Canvas(filename, pagesize=letter)
    c.drawString(100, 750, "District Crop Yield Report")
    y = 700
    for key, value in input_data.items():
        c.drawString(100, y, f"{key}: {value}")
        y -= 20
    if prediction:
        c.drawString(100, y, f"Predicted Yield: {prediction:.2f} Kg/ha")
    c.save()
    
    return send_file(filename, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)