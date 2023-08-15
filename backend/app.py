# backend/app.py
from flask import Flask, render_template, request, jsonify
import pickle
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data = request.json

    if 'text' in data:
        text = data['text']
        print(text)

        response = {
            'sentiment': "neutral",
            'entities': []  # Replace with entity extraction logic
        }
        return jsonify(response)
    else:
        return jsonify({'error': 'Invalid input'}), 400

if __name__ == '__main__':
    app.run(debug=True)
