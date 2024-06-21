from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

# Load the pre-trained model and scaler
model = joblib.load('crop_prediction_model1_v2.pkl')
scaler = joblib.load('scaler1_v2.pkl')

weather_api_key = '14a20a42870c19871e751b16f83176a9'
geolocator = Nominatim(user_agent="crop_recommendation_app")

# Route for home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to fetch weather and location data
@app.route('/get_location_data', methods=['POST'])
def get_location_data():
    data = request.get_json()
    latitude = data['latitude']
    longitude = data['longitude']

    try:
        # Fetch location name using reverse geocoding
        location = geolocator.reverse((latitude, longitude), exactly_one=True)
        location_name = location.address

        # Fetch live weather data from OpenWeatherMap API
        weather_url = f'http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={weather_api_key}&units=metric'
        response = requests.get(weather_url)

        if response.status_code == 200:
            weather_data = response.json()
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            rainfall = weather_data['rain']['1h'] if 'rain' in weather_data else 0

            return jsonify({
                'location_name': location_name,
                'temperature': temperature,
                'humidity': humidity,
                'rainfall': rainfall
            })
        else:
            return jsonify({'error': 'Failed to fetch weather data'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route for prediction
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        try:
            # Get values from the form
            N = float(request.form['N'])
            P = float(request.form['P'])
            K = float(request.form['K'])
            ph = float(request.form['ph'])
            temperature = float(request.form['temperature'])
            humidity = float(request.form['humidity'])
            rainfall = float(request.form['rainfall'])

            # Scale input features
            scaled_input = scaler.transform([[N, P, K, ph, temperature, humidity, rainfall]])

            # Predict using the model
            predicted_crop = model.predict(scaled_input)
            print("User Inputs:", N, P, K, ph, temperature, humidity, rainfall)
            print("Scaled Input:", scaled_input)

            # Render result template with predicted crop and user inputs
            return render_template('result.html', crop=predicted_crop[0],
                                   N=N, P=P, K=K, ph=ph,
                                   temperature=temperature, humidity=humidity, rainfall=rainfall)

        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
