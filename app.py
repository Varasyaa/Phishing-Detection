from flask import Flask, request, jsonify
import joblib
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from flask_cors import CORS
import os

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Load the trained phishing email detection model
model = joblib.load("models/phishing_model.pkl")
vectorizer = joblib.load("models/vectorizer.pkl")

# Ensure NLTK resources are available
nltk.download('stopwords')
nltk.download('punkt')

# Text preprocessing function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'http\S+', '', text)  # Remove URLs
    text = re.sub(r'[^a-zA-Z\s]', '', text)  # Remove special characters
    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word not in stopwords.words('english') and word not in string.punctuation]
    return ' '.join(tokens)

@app.route('/detect_phishing', methods=['POST'])
def detect_phishing():
    data = request.get_json()
    if 'email_content' not in data:
        return jsonify({"error": "Missing email content"}), 400
    
    email_text = data['email_content']
    processed_text = preprocess_text(email_text)
    vectorized_text = vectorizer.transform([processed_text])
    prediction = model.predict(vectorized_text)
    
    result = "Phishing Email Detected" if prediction[0] == 1 else "Legitimate Email"
    
    return jsonify({
        "email_content": email_text,
        "prediction": result
    })

if __name__ == '__main__':
    app.run(debug=True)
