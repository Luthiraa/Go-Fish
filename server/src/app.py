from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/github', methods=['GET'])
def get_github_data():
    sample_data = {
        "endpoint": "https://github.com/Luthiraa"
    }
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(debug=True)