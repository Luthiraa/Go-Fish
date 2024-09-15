from flask import Flask, jsonify, request
from flask_cors import CORS
from services.search_and_summarize import process_search_and_summarize, extract_important_words
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
        summary, detailed_summary, resources, image_url, reddit_embed, github_url, github_line_number, github_snippet, matching_products = process_search_and_summarize(query)
        important = extract_important_words(query)
        logging.debug(f"Summary: {summary}")
        logging.debug(f"Important: {important}")
        logging.debug(f"Resources: {resources}")
        logging.debug(f"Reddit Embed: {reddit_embed}")
        logging.debug(f"Snippet: {github_snippet}")
        logging.debug(f"Line Number: {github_line_number}")
        logging.debug(f"File URL: {github_url}")
        return jsonify({
            "summary": summary,
            "detailed_summary": detailed_summary,
            "resources": resources,
            "important": important,
            "image_url": image_url,
            "reddit_embed": reddit_embed,
            "snippet": github_snippet,
            "line_number": github_line_number,
            "file_url": github_url,
            "matching_products": matching_products
        })
    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500
if __name__ == '__main__':
    app.run(debug=True)