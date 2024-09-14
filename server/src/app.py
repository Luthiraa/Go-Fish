from flask import Flask, jsonify, request
from flask_cors import CORS
from github_search import search_code_with_gpt

app = Flask(__name__)
CORS(app)

@app.route('/api/github', methods=['GET'])
def get_github_data():
    query = request.args.get('query')
    repo_name = request.args.get('repo_name')
    github_token = request.args.get('github_token')

    if not query or not repo_name or not github_token:
        return jsonify({"error": "Missing query, repo_name, or github_token"}), 400

    try:
        results = search_code_with_gpt(query, repo_name, github_token)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)