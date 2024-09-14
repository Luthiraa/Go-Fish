from flask import Flask, jsonify, request
from flask_cors import CORS
from services.search_and_summarize import process_search_and_summarize
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/api/search_and_summarize', methods=['POST'])
def search_and_summarize():
    data = request.get_json()
    query = data.get('query')
    
    # Sample query for testing
    if not query:
        query = "dog water"
    
    logging.debug(f"Received query: {query}")
    
    try:
        summary, resources = process_search_and_summarize(query)
        logging.debug(f"Summary: {summary}")
        logging.debug(f"Resources: {resources}")
        return jsonify({"summary": summary, "resources": resources})
    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)