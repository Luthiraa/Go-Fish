import requests
from flask import request, jsonify
from github import Github

app = Flask(__name__)

app.route('/')

@app.route('/repos', methods=['GET'])
def list_repos():
    token = request.args.get('token')
    if not token:
        return jsonify({"error": "Token is required"}), 400

    g = Github(token)
    user = g.get_user()
    repos = [{"name": repo.name, "url": repo.html_url} for repo in user.get_repos()]

    return jsonify(repos)

if __name__ == '__main__':
    app.run()





    

    