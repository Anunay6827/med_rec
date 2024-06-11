import os
import logging
from flask import Flask, request, render_template, jsonify
import pandas as pd
from joblib import load
from sklearn.metrics import jaccard_score
import google.generativeai as genai
from PIL import Image
import pathlib
import random

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['DEBUG'] = True

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# Load the pre-trained model and the medicine dataset
try:
    kmeans = load('kmeans_model.joblib')
    logging.info("KMeans model loaded successfully.")
except Exception as e:
    logging.error("Error loading KMeans model: %s", e)
    raise

try:
    medicine = pd.read_csv('medicine.csv')
    logging.info("Medicine dataset loaded successfully.")
except Exception as e:
    logging.error("Error loading medicine dataset: %s", e)
    raise

# Configure the Google Generative AI API
GOOGLE_API_KEY = 'AIzaSyDxrtUp6CYVNbKGRRIp0NtV6fMArVZf3Bg'
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')

def recommend_alternatives(medicine_name):
    try:
        selected_cluster = medicine[medicine['name'] == medicine_name]['Cluster'].iloc[0]
        cluster_medicines = medicine[medicine['Cluster'] == selected_cluster]['name']
        selected_set = set(medicine_name)
        cluster_sets = [set(name) for name in cluster_medicines]
        similarities = [(jaccard_score(selected_set, med_set), med_name)
                        for med_set, med_name in zip(cluster_sets, cluster_medicines)]
        sorted_similarities = sorted(similarities, reverse=True)
        top_5_medicines = [med_name for similarity, med_name in sorted_similarities[:6] if med_name != medicine_name][:5]
        return top_5_medicines
    except Exception as e:
        logging.error("Error recommending alternatives: %s", e)
        return []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'prescription' not in request.files:
            return jsonify({'error': 'No file part'})

        file = request.files['prescription']
        if file.filename == '':
            return jsonify({'error': 'No selected file'})

        if file:
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            logging.info("File saved to %s", filepath)

            img = Image.open(filepath)
            prompt = "Analyze the image."
            response = model.generate_content([prompt, img], stream=True)
            response.resolve()
            medicines = response.text.split('\n')  # Assuming the response lists the medicines line by line

            recommendations = {}
            for med in medicines:

                alternatives = recommend_alternatives(med)
                random.shuffle(alternatives)
                recommendations[med] = alternatives[:5]

            return jsonify({'medicines': medicines, 'recommendations': recommendations})
    except Exception as e:
        logging.error("Error processing upload: %s", e)
        return jsonify({'error': 'An error occurred during processing.'})

if __name__ == '__main__':
    app.run(debug=True)
