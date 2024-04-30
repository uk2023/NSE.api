from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

def preprocess_data(json_data, expiry_date):
    try:
        ce_data = json_data['filtered']['CE']
        pe_data = json_data['filtered']['PE']
        option_data = json_data['filtered']['data']
        
        processed_data = {
            'CE': ce_data,
            'PE': pe_data,
            'optionData': option_data,
            'expiryDate': expiry_date,
        }
        return processed_data
    except KeyError as e:
        raise ValueError(f"Invalid JSON data format: {e}")

@app.route('/api/nseData')
def get_nse_data():
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get('https://www.nseindia.com/api/option-chain-indices?symbol=NIFTY', headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        
        json_data = response.json()
        processed_data = preprocess_data(json_data, '09-May-2024')
        
        return jsonify(processed_data)
    except requests.RequestException as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
