from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/capitalize', methods=['POST'])
def capitalize_text():
    data = request.get_json()
    input_text = data['inputText']
    capitalized_text = input_text.upper()
    return jsonify({'capitalizedText': "Divya Singh"})

if __name__ == '__main__':
    app.run()
