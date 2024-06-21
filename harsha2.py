from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib
import pandas as pd
import requests
from sklearn.preprocessing import StandardScaler
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

model = joblib.load('venv\crop_prediction_model_v2.pkl')
scaler = joblib.load('venv\scaler_v2.pkl')

weather_api_key = '14a20a42870c19871e751b16f83176a9'

geolocator = Nominatim(user_agent="crop_recommendation_app")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
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

            input_data = pd.DataFrame({
                'humidity': [humidity],
                'rainfall': [rainfall],
                'temperature': [temperature]
            })

            input_data_scaled = scaler.transform(input_data)
            prediction = model.predict(input_data_scaled)[0]

            return jsonify({
                'prediction': prediction,
                'location_name': location_name
            })
        else:
            return jsonify({'error': 'Failed to fetch weather data'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
