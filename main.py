from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import json

app = Flask(__name__, static_folder='templates')
CORS(app)

BASE_URL = "https://www.carqueryapi.com/api/0.3/?callback=?"
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
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
    except Exception as e:
        print(f"Error: {e}")
    return {}

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/makes')
def get_makes():
    year = request.args.get('year')
    sold_in_us = request.args.get('sold_in_us')
    url = f"{BASE_URL}&cmd=getMakes"
    if year:
        url += f"&year={year}"
    if sold_in_us == '1':
        url += "&sold_in_us=1"
    return jsonify(fetch_jsonp(url).get('Makes', []))

@app.route('/models')
def get_models():
    year = request.args.get('year')
    make = request.args.get('make')
    sold_in_us = request.args.get('sold_in_us')
    url = f"{BASE_URL}&cmd=getModels&make={make}"
    if year:
        url += f"&year={year}"
    if sold_in_us == '1':
        url += "&sold_in_us=1"
    return jsonify(fetch_jsonp(url).get('Models', []))

@app.route('/trims')
def get_trims():
    year = request.args.get('year')
    make = request.args.get('make')
    model = request.args.get('model')
    sold_in_us = request.args.get('sold_in_us')
    url = f"{BASE_URL}&cmd=getTrims&make={make}&model={model}"
    if year:
        url += f"&year={year}"
    if sold_in_us == '1':
        url += "&sold_in_us=1"
    return jsonify(fetch_jsonp(url).get('Trims', []))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
