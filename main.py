from flask import Flask, request, jsonify,send_from_directory
from flask_cors import CORS
import requests
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def serve_index():
    return send_from_directory('templates', 'index.html')


BASE_URL = "https://www.carqueryapi.com/api/0.3/?callback=?"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36'
}

def fetch_jsonp(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            raw = response.text.strip()
            if raw.startswith('?('):
                raw = raw[2:]
            if raw.endswith(');'):
                raw = raw[:-2]
            return json.loads(raw)
        else:
            print(f"❌ HTTP {response.status_code}: {url}")
    except Exception as e:
        print(f"⚠️ Error: {e} for URL: {url}")
    return {}

@app.route('/makes')
def get_makes():
    year = request.args.get('year')
    sold_in_us = request.args.get('sold_in_us')
    url = f"{BASE_URL}&cmd=getMakes"
    if year:
        url += f"&year={year}"
    if sold_in_us == '1':
        url += "&sold_in_us=1"
    data = fetch_jsonp(url)
    return jsonify(data.get('Makes', []))

@app.route('/models')
def get_models():
    year = request.args.get('year')
    make = request.args.get('make')
    sold_in_us = request.args.get('sold_in_us')
    if not make:
        return jsonify([])

    url = f"{BASE_URL}&cmd=getModels&make={make}"
    if year:
        url += f"&year={year}"
    if sold_in_us == '1':
        url += "&sold_in_us=1"
    data = fetch_jsonp(url)
    return jsonify(data.get('Models', []))

@app.route('/trims')
def get_trims():
    year = request.args.get('year')
    make = request.args.get('make')
    model = request.args.get('model')
    sold_in_us = request.args.get('sold_in_us')
    if not make or not model:
        return jsonify([])

    url = f"{BASE_URL}&cmd=getTrims&make={make}&model={model}"
    if year:
        url += f"&year={year}"
    if sold_in_us == '1':
        url += "&sold_in_us=1"
    data = fetch_jsonp(url)
    return jsonify(data.get('Trims', []))

if __name__ == '__main__':
    app.run(debug=True)
