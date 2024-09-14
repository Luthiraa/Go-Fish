from flask import Flask, request, jsonify
import openai
from github import Github

app = Flask(__name__)

# Initialize OpenAI with your API key
openai.api_key = "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"

def get_repo_contents(repo):
    contents = repo.get_contents("")
    all_files = []

    def recursive_fetch(contents):
        for content_file in contents:
            if content_file.type == "dir":
                recursive_fetch(repo.get_contents(content_file.path))
            else:
                all_files.append(content_file)

    recursive_fetch(contents)
    return all_files

def check_relevance_with_gpt(query, line):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that helps search code repositories."},
            {"role": "user", "content": f"Does the following code match this query?\nQuery: {query}\nCode: {line}"}
        ]
    )
    return response['choices'][0]['message']['content'].strip()

def search_code_with_gpt(query, repo_name, github_token):
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    all_files = get_repo_contents(repo)
    search_results = []

    for content_file in all_files:
        file_content = repo.get_contents(content_file.path).decoded_content.decode('utf-8', errors='ignore')
        lines = file_content.split('\n')
        
        for line_num, line in enumerate(lines, start=1):
            if line.strip():
                relevance = check_relevance_with_gpt(query, line)
                if "yes" in relevance.lower() or "relevant" in relevance.lower():
                    search_results.append({
                        'file_path': content_file.path,
                        'line_number': line_num,
                        'code_snippet': line.strip(),
                        'gpt_response': relevance
                    })

    return search_results

@app.route('/search', methods=['POST'])
def search():
    data = request.json
    query = data.get('query')
    repo_name = data.get('repo_name')
    github_token = data.get('github_token')
    results = search_code_with_gpt(query, repo_name, github_token)
    return jsonify(results)

@app.route('/api/github', methods=['GET'])
def get_github_data():
    sample_data = {
        "endpoint": "https://github.com/Luthiraa "
    }
    return jsonify(sample_data)

if __name__ == '__main__':
    app.run(debug=True)