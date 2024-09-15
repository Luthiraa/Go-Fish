from flask import Flask, jsonify, request
from flask_cors import CORS
from services.search_and_summarize import process_search_and_summarize
from services.search_and_summarize import extract_important_words
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
        summary, resources, image_url, reddit_embed, github_results = process_search_and_summarize(query)
        important = extract_important_words(query)
        logging.debug(f"Summary: {summary}")
        logging.debug(f"Important: {important}")
        logging.debug(f"Resources: {resources}")
        logging.debug(f"Reddit Embed: {reddit_embed}")
        return jsonify({
            "summary": summary,
            "resources": resources,
            "important": important,
            "image_url": image_url,
            "reddit_embed": reddit_embed,
            "github_results": github_results, 

        })
    except Exception as e:
        logging.error("Error occurred: %s", str(e))
        return jsonify({"error": str(e)}), 500

# @app.route('/api/github_search', methods=['POST'])
# def github_search():
#     data = request.get_json()s
#     query = data.get('query')
#     github_link = data.get('githubLink')
    
#     if not query or not github_link:
#         return jsonify({"error": "Query and GitHub link are required"}), 400
    
#     logging.debug(f"Received GitHub search query: {query} for repository: {github_link}")
    
#     try:
#         result = search_github_code(query, github_link)
#         if result:
#             snippet, line_number, file_url = result
#             return jsonify({
#                 "snippet": snippet,
#                 "line_number": line_number,
#                 "file_url": file_url
#             })
#         else:
#             return jsonify({"error": "No results found"}), 404
#     except Exception as e:
#         logging.error("Error occurred during GitHub search: %s", str(e))
#         return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)