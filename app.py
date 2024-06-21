from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
import pandas as pd
import joblib
import numpy as np
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)
CORS(app)

data = pd.read_csv(r'venv/Fertilizer.csv')

# Remove values within parentheses from crop names
data['Crop'] = data['Crop'].apply(lambda x: x.split('(')[0].strip())

print(data["Crop"].unique())

fertilizer_dic = {
    'NHigh': [
        "మీ మట్టిలో N విలువ అధికంగా ఉంది మరియు కలుపు మొక్కలు ఉత్పన్నమవుతాయి.",
        "పేడను జోడించండి.",
        "కాఫీ గ్రిండ్‌లు ఉపయోగించండి.",
        "నైట్రోజన్ స.fix.స్.క మొక్కలు నాటండి.",
        "హరిత పేడ పంటలు నాటండి.",
        "పంటలను పెంచేటప్పుడు మల్చ్ ఉపయోగించండి."
    ],
    'Nlow': [
        "మీ మట్టిలో N విలువ తక్కువగా ఉంది.",
        "సాదస్ట్ను లేదా తేలికపాటి చెక్కలను జోడించండి.",
        "బరువైన నైట్రోజన్ తినే మొక్కలను నాటండి.",
        "నీటితో రాచడం.",
        "చక్కర జోడించండి.",
        "మట్టిలో కంపోస్ట్ చేయబడిన పేడను జోడించండి.",
        "నైట్రోజన్ స.fix.స్.క మొక్కలు నాటండి.",
        "ఎన్పీకే ఫర్టిలైజర్లు అధిక N విలువతో ఉపయోగించండి.",
        "ఏమీ చేయవద్దు."
    ],
    'PHigh': [
        "మీ మట్టిలో P విలువ అధికంగా ఉంది.",
        "పేడను జోడించడం నివారించండి.",
        "పాస్పరస్-రహిత ఎరువు ఉపయోగించండి.",
        "మీ మట్టిని నీటితో రాచండి.",
        "పాస్పరస్ పెంచకుండా నైట్రోజన్ పెంచడానికి పుష్టికర కూరగాయలను నాటండి.",
        "పాస్పరస్ స్థాయిలను తగ్గించడానికి పంటలు మారుస్తూ ఉండండి."
    ],
    'Plow': [
        "మీ మట్టిలో P విలువ తక్కువగా ఉంది.",
        "ఎముకల పిండం జోడించండి.",
        "రాక్ ఫాస్పేట్ ఉపయోగించండి.",
        "ఫాస్పరస్ ఎరువులు ఉపయోగించండి.",
        "సేంద్రియ కంపోస్ట్ జోడించండి.",
        "పేడ జోడించండి.",
        "మట్టిలో మట్టిని జోడించండి.",
        "మట్టిని సరైన pHలో ఉంచండి.",
        "మట్టిలో pH తక్కువగా ఉంటే, చునాకు లేదా పొటాషియం కార్బోనేట్‌ను జోడించండి.",
        "pH అధికంగా ఉంటే, ఆమ్లీకరించే ఎరువులు జోడించండి."
    ],
    'KHigh': [
        "మీ మట్టిలో K విలువ అధికంగా ఉంది.",
        "పేడను జోడించడం నివారించండి.",
        "పొటాషియం నిత్యాహారాలను నాటండి.",
        "పొటాషియం నియామక సిలిండరులు నాటండి.",
        "కాస్టర్ ఎరువులు నాటండి.",
        "మినరల్ రాక్ మరియు కాస్టర్ ఎరువులు నాటండి.",
        "నాటి పారుదలో పొటాషియం నిత్యాహారాలను నాటండి."
    ],
    'Klow': [
        "మీ మట్టిలో K విలువ తక్కువగా ఉంది.",
        "కాస్టర్ ఎరువులు నాటండి.",
        "పేడను జోడించండి.",
        "నైట్రోజన్ మరియు పొటాషియం ప్రయోగించే ఎరువులు నాటండి.",
        "మీ మట్టిలో ఫాస్ఫరస్ లేదా కాల్షియం ఉంటే, అవి తినిపించుకుని ఉంచుకోవడం సూచించండి."
    ]
}


def get_fertilizer_recommendation(crop):
    crop_data = data[data['Crop'].str.lower() == crop.lower()]
    if not crop_data.empty:
        crop_data = crop_data.iloc[0]
    else:
        return "Crop not found in data."

    recommendations = []
    if crop_data['N'] > 50:
        recommendations.extend(fertilizer_dic['NHigh'])
    else:
        recommendations.extend(fertilizer_dic['Nlow'])

    if crop_data['P'] > 40:
        recommendations.extend(fertilizer_dic['PHigh'])
    else:
        recommendations.extend(fertilizer_dic['Plow'])

    if crop_data['K'] > 40:
        recommendations.extend(fertilizer_dic['KHigh'])
    else:
        recommendations.extend(fertilizer_dic['Klow'])

    return recommendations


@app.route('/')
def index():
    api_key = "a02dfc95b24e4fc8a32b594867583e1a"
    query = "agriculture OR disaster"
    url = f"https://newsapi.org/v2/everything?q={query}&language=en&sortBy=publishedAt&apiKey={api_key}"

    response = requests.get(url)
    news_data = response.json()

    articles = news_data.get('articles', [])

    if articles:
        # Filter articles to only include those that mention India
        filtered_articles = [article for article in articles if article.get('title') and 'India' in article['title'] or article.get('description') and 'India' in article['description']]
    else:
        filtered_articles = []

    return render_template('index2.html', articles=filtered_articles)

@app.route('/nosoil')
def index1():
    return render_template('index1.html')

@app.route('/fertirecommend')
def fertirecommend():
    return render_template('frty9.html')

@app.route('/recommend', methods=['POST'])
def get_recommendation():
    crop = request.form['crop']
    recommendations = get_fertilizer_recommendation(crop)
    return render_template('recommendations.html', crop=crop, recommendations=recommendations)

# Load the pre-trained model and scaler for 7 features
model = joblib.load('venv/crop_prediction_model1_v2.pkl')
scaler = joblib.load('venv/scaler1_v2.pkl')

weather_api_key = '14a20a42870c19871e751b16f83176a9'
geolocator = Nominatim(user_agent="crop_recommendation_app")

@app.route('/direct')
def index2():
    return render_template('index3.html')

@app.route('/li')
def vijay():
    return render_template('l1.html', image_url="https://www.canr.msu.edu/contentAsset/image/75cb09cb3398678dbf99321d744d2224/fileAsset/filter/Resize/resize_w/600")

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

# Load the pre-trained model and scaler for 3 features
model_3features = joblib.load('venv/crop_prediction_model_v2.pkl')
scaler_3features = joblib.load('venv/scaler_v2.pkl')

@app.route('/predict1', methods=['POST'])
def predict1():
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

            input_data_scaled = scaler_3features.transform(input_data)
            prediction = model_3features.predict(input_data_scaled)[0]

            return jsonify({
                'prediction': prediction,
                'location_name': location_name
            })
        else:
            return jsonify({'error': 'Failed to fetch weather data'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500
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




if __name__ == '__main__':
    app.run(debug=True)
