# Crop Yield Prediction System

The Crop Yield Prediction System is a Flask-based web application designed to predict crop yields, analyze historical trends, and recommend optimal crops using weather, soil, and regional data. Built with machine learning, the system empowers farmers, policymakers, and agricultural stakeholders with data-driven insights to optimize productivity and promote sustainable farming practices. The application features a user-friendly interface, robust error handling, and geographical visualization, making it accessible and practical for diverse users.

## Features

- **Crop Yield Prediction**: Forecast crop yields based on inputs like crop type, year, season, state, area, production, rainfall, fertilizer, and pesticide usage using a pre-trained machine learning model.
- **Geographical Visualization**: Display prediction results on a map using state-specific coordinates for spatial context.
- **Historical Trend Analysis**: Analyze historical yield trends for specific crops and states, aiding long-term planning.
- **Crop Recommendations**: Suggest the top three crops for a given state and season based on historical yield performance.
- **User-Friendly Interface**: Intuitive web forms and result pages for easy interaction, built with Flask templates.
- **Robust Error Handling**: Comprehensive validation and error messages to ensure reliability and user guidance.

## Technologies Used

- **Python**: Version 3.8+ for backend logic and data processing.
- **Flask**: Version 2.0+ for web framework, routing, and template rendering.
- **scikit-learn**: Version 1.2+ for loading the pre-trained model and encoders.
- **pandas**: Version 1.5+ for data manipulation and CSV processing.
- **NumPy**: Version 1.23+ for numerical computations.
- **Werkzeug**: Version 2.0+ (bundled with Flask) for HTTP request handling.
- **HTML/CSS**: For front-end templates and styling.
- **JavaScript (Optional)**: For potential map or chart visualizations (e.g., Leaflet.js, Chart.js).
- **CSV**: For storing historical data (`crop_yield_data.csv`).

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

   - Ensure `model.pkl` (pre-trained model) and `encoders.pkl` (categorical encoders) are placed in the project root.
   - Place `crop_yield_data.csv` in the `data/` directory. The CSV should include columns: `Crop`, `Crop_Year`, `Season`, `State`, `Area`, `Production`, `Annual_Rainfall`, `Fertilizer`, `Pesticide`, `Yield`.

5. **Run the Application**:

   ```bash
   python app.py
   ```

   - The app will run in debug mode at `http://127.0.0.1:5000/`.

6. **Access the Application**:

   - Open a web browser and navigate to `http://127.0.0.1:5000/` to access the homepage.

## Project Structure

```plaintext
crop-yield-prediction/
├── data/
│   └── crop_yield_data.csv      # Historical crop yield data
├── templates/
│   ├── index.html               # Homepage with input form
│   ├── result.html              # Prediction results with map
│   ├── trends.html              # Trend analysis page
│   └── recommend.html           # Crop recommendation page
├── app.py                       # Main Flask application
├── model.pkl                    # Pre-trained ML model
├── encoders.pkl                 # Categorical encoders
├── requirements.txt             # Python dependencies
└── README.md                    # Project documentation
```

## Usage

1. **Predict Crop Yield**:

   - Navigate to the homepage (`/`).
   - Enter crop details (e.g., crop type, state, rainfall) in the form.
   - Submit to view the predicted yield and a map of the selected state.

2. **Analyze Trends**:

   - Go to the trends page (`/trends`).
   - Select a crop and state to view historical yield data by year.

3. **Get Crop Recommendations**:

   - Visit the recommendations page (`/recommend`).
   - Choose a state and season to see the top three crops with the highest average yields.

## Deployment

For production deployment:

- Use a WSGI server like **Gunicorn**:

  ```bash
  gunicorn -w 4 app:app
  ```
- Set up a reverse proxy with **Nginx** or **Apache** for static file serving and load balancing.
- Secure the app with an SSL/TLS certificate (e.g., Let’s Encrypt).
- Host on a cloud platform (e.g., AWS, Heroku, or Azure) for scalability.
- Ensure `model.pkl`, `encoders.pkl`, and `crop_yield_data.csv` are securely stored with restricted permissions.

## Future Enhancements

- Integrate real-time weather APIs for dynamic rainfall and temperature data.
- Add a database (e.g., SQLite, PostgreSQL) for scalable data storage.
- Enhance visualizations with interactive charts (e.g., Plotly) and dynamic maps.
- Develop a mobile app for offline access and push notifications.
- Support multi-language interfaces for broader accessibility.
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

For questions or feedback, contact \[coderofml143@gmail.com\] or open an issue on GitHub.

---

*Built with 🌾 for sustainable agriculture.*