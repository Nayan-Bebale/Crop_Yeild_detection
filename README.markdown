# Crop Yield Prediction System

The Crop Yield Prediction System is a Flask-based web application designed to predict crop yields, analyze historical trends, and recommend optimal crops using weather, soil, and regional data. Leveraging machine learning, this system provides farmers, policymakers, and agricultural stakeholders with actionable, data-driven insights to enhance productivity and support sustainable farming. It offers a user-friendly interface, robust error handling, and advanced visualizations for practical and accessible use.

## Features

- **Crop Yield Prediction**
  - Forecast yields using a machine learning model with inputs such as crop type, year, season, state/district, area, production, rainfall, fertilizer, and pesticide.
  - **New:** District-level predictions for more localized and granular insights.

- **Geographical Visualization**
  - Interactive maps displaying prediction results using state and district coordinates.
  - **New:** Enhanced with district-level coordinates for precise location mapping.

- **Historical Trend Analysis**
  - Analyze historical yield data for specific crops and regions.
  - **New:** Multi-crop trend visualization for comparative analysis in a single chart.

- **Crop Recommendations**
  - Suggest the top three crops for a given state and season based on historical yield performance.

- **Data Insights and Analytics**
  - **New:** Interactive dashboard featuring:
    - Bar charts for average crop yields.
    - Histograms for yield distribution.
    - Pie charts for production share by crop.
    - Scatter plots for area vs. yield analysis.
    - Tables highlighting top-performing districts.
    - Filters for dynamic data exploration by year and crop.

- **Downloadable Reports**
  - **New:** Export prediction results and insights as PDF reports for district-level data.

- **User-Friendly Interface**
  - Intuitive web forms and result pages for seamless user interaction.

- **Robust Error Handling**
  - Comprehensive input validation and clear error messages to guide users effectively.

## Technologies Used

- **Python**: Version 3.8+ for backend logic and data processing.
- **Flask**: Version 2.0+ for web framework, routing, and template rendering.
- **scikit-learn**: Version 1.2+ for machine learning models and categorical encoders.
- **pandas**: Version 1.5+ for data manipulation and analysis.
- **NumPy**: Version 1.23+ for numerical computations.
- **Werkzeug**: Version 2.0+ (bundled with Flask) for HTTP request handling.
- **HTML/CSS**: For front-end templates and styling.
- **JavaScript**:
  - **Chart.js**: For interactive data visualizations in the dashboard.
  - **Leaflet.js**: For enhanced geographical map visualizations.
- **CSV**: For storing historical and district-level data.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)
- Web browser (e.g., Chrome, Firefox, Edge)

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/your-username/crop-yield-prediction.git
   cd crop-yield-prediction
   ```

2. **Create a Virtual Environment** (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Model and Data Files**:

   - Place `model.pkl` (pre-trained model) and `encoders.pkl` (categorical encoders) in the project root.
   - Add `crop_yield_data.csv` and `Ind_adm2_Points.csv` to the `data/` directory:
     - `crop_yield_data.csv`: Historical crop yield data with columns like `Crop`, `Crop_Year`, `Season`, `State`, `Area`, `Production`, `Annual_Rainfall`, `Fertilizer`, `Pesticide`, `Yield`.
     - `Ind_adm2_Points.csv`: District coordinates with columns `District`, `Latitude`, `Longitude`.

5. **Run the Application**:

   ```bash
   python app.py
   ```

   - The app will launch in debug mode at `http://127.0.0.1:5000/`.

6. **Access the Application**:

   - Open a web browser and visit `http://127.0.0.1:5000/` to explore the homepage.

## Project Structure

```plaintext
crop-yield-prediction/
├── data/
│   ├── crop_yield_data.csv      # Historical crop yield data
│   └── Ind_adm2_Points.csv      # District coordinates data
├── templates/
│   ├── index.html               # Homepage with input form
│   ├── result.html              # Prediction results with map
│   ├── trends.html              # Trend analysis page
│   ├── recommend.html           # Crop recommendation page
│   ├── insights.html            # Dashboard for data insights
│   └── other templates for district-level features
├── app.py                       # Main Flask application
├── model.pkl                    # Pre-trained ML model
├── encoders.pkl                 # Categorical encoders
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## Usage

1. **Predict Crop Yield**:

   - Visit the homepage (`/`).
   - Input crop details (e.g., crop type, state, rainfall) in the form.
   - Submit to see the predicted yield and a map of the selected region.

2. **Analyze Trends**:

   - Navigate to the trends page (`/trends`).
   - Select a crop and state to view historical yield trends by year.

3. **Get Crop Recommendations**:

   - Go to the recommendations page (`/recommend`).
   - Choose a state and season to receive the top three crop suggestions.

4. **Explore Data Insights**:

   - Access the insights dashboard (`/dist_insights`).
   - Apply filters for year and crop to interact with visualizations and analytics.

5. **District-Level Features**:

   - Use the navigation menu to explore district-wise predictions, trends, comparisons, and insights.

## Deployment

For production deployment:

- Use a WSGI server like **Gunicorn**:

  ```bash
  gunicorn -w 4 app:app
  ```

- Configure a reverse proxy with **Nginx** or **Apache** for static file serving and load balancing.
- Secure the app with an SSL/TLS certificate (e.g., Let’s Encrypt).
- Deploy on a cloud platform (e.g., AWS, Heroku, Azure) for scalability.
- Ensure `model.pkl`, `encoders.pkl`, and data files are stored securely with restricted permissions.

## Future Enhancements

- Integrate real-time weather APIs for dynamic rainfall and temperature inputs.
- Implement a database (e.g., SQLite, PostgreSQL) for scalable data management.
- Enhance visualizations with advanced tools like Plotly for interactivity.
- Develop a mobile app with offline access and push notifications.
- Add multi-language support for broader accessibility.
- Incorporate IoT sensor data for real-time soil and weather monitoring.

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request with a detailed description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or feedback, reach out to [coderofml143@gmail.com] or open an issue on GitHub.

---

*Built with 🌾 for sustainable agriculture.*
