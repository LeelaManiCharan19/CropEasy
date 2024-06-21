from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

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
    return render_template('index1.html')

@app.route('/fertirecommend')
def fertirecommend():
    return render_template('frty9.html')


@app.route('/recommend', methods=['POST'])
def get_recommendation():
    crop = request.form['crop']
    recommendations = get_fertilizer_recommendation(crop)
    return render_template('recommendations.html', crop=crop, recommendations=recommendations)


if __name__ == '__main__':
    app.run(debug=True)
