from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import extract_features
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

model = joblib.load('phishing_model.pkl')
client = MongoClient("mongodb://localhost:27017/")
db = client.phishing
logs = db.logs

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    url = data['url']
    features = extract_features.extract(url)
    prediction = model.predict([features])[0]

    logs.insert_one({"url": url, "features": features, "result": int(prediction)})

    return jsonify({"phishing": bool(prediction)})

if __name__ == "__main__":
    app.run(debug=True)
