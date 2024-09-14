from flask import Flask, jsonify, request
from flask_cors import CORS
from services.github_search import search_code_with_gpt
from services.summary import summarize_search_query
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/github', methods=['GET'])
def get_github_data():
    github_token = "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"
    repo_name = "Luthiraa/Go-Fish"
    query = "function to add two numbers"

    if not query or not repo_name or not github_token:
        return jsonify({"error": "Missing query, repo_name, or github_token"}), 400

    try:
        results = search_code_with_gpt(query, repo_name, github_token)
        return jsonify(results)
    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

@app.route('/api/summarize', methods=['GET'])
def get_summary():
    query = request.args.get('query')

    if not query:
        return jsonify({"error": "Missing query parameter"}), 400

    try:
        summaries = summarize_search_query(query)
        return jsonify(summaries)
    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)