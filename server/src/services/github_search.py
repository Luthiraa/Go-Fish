import openai
from github import Github
import secrets

# Initialize OpenAI with your API key
openai.api_key = secrets.openai_api

def search_code_with_gpt(query, repo_name, github_token):
    """
    Searches for the most relevant code snippet in the given GitHub repository using GPT-3.5.
    
    :param query: The query string to search for.
    :param repo_name: The name of the GitHub repository in the form 'owner/repo'.
    :param github_token: Your GitHub API token for authentication.
    :return: A list of dictionaries containing the file path, code snippet, and line number.
    """
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    contents = repo.get_contents("")
    search_results = [] 
    
    def recursive_search(contents):
        for content_file in contents:
            if content_file.type == "dir":
                # If it's a directory, fetch contents recursively
                recursive_search(repo.get_contents(content_file.path))
            else:
                # If it's a file, retrieve the file contents
                file_content = repo.get_contents(content_file.path).decoded_content.decode('utf-8', errors='ignore')
                lines = file_content.split('\n')
                
                # For each line, send the query and line of code to GPT-3.5
                for line_num, line in enumerate(lines, start=1):
                    if line.strip():  # Skip empty lines
                        response = openai.ChatCompletion.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that helps search code repositories."},
                                {"role": "user", "content": f"Does the following code match this query?\nQuery: {query}\nCode: {line}"}
                            ]
                        )
                        relevance = response['choices'][0]['message']['content'].strip()
                        
                        # If GPT indicates a match or relevance, record it
                        if "yes" in relevance.lower() or "relevant" in relevance.lower():
                            search_results.append({
                                'file_path': content_file.path,
                                'line_number': line_num,
                                'code_snippet': line.strip(),
                                'gpt_response': relevance
                            })
    
    # Start recursive search
    recursive_search(contents)

    return search_results

# Example usage
if __name__ == "__main__":
    github_token = "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"
    repo_name = "Luthiraa/Go-Fish"
    query = "function to add two numbers"

    results = search_code_with_gpt(query, repo_name, github_token)

    # Print the results
    for result in results:
        print(f"Found in {result['file_path']} at line {result['line_number']}:")
        print(f"Code: {result['code_snippet']}")
        print(f"GPT-3.5 Relevance: {result['gpt_response']}")
        print("-" * 40)