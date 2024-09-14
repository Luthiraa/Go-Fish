from groq import Groq
from github import Github
import secrets

# Set your Groq API key directly in the script
api_key = "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"

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)

def search_code_with_gpt(query, repo_name, github_token):
    """
    Searches for the most relevant code snippet in the given GitHub repository using Groq.
    
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
                
                # For each line, send the query and line of code to Groq
                for line_num, line in enumerate(lines, start=1):
                    if line.strip():  # Skip empty lines
                        response = client.chat.completions.create(
                            model="llama3-8b-8192",
                            messages=[
                                {"role": "system", "content": "You are a helpful assistant that helps search code repositories."},
                                {"role": "user", "content": f"Does the following code match this query?\nQuery: {query}\nCode: {line}"}
                            ]
                        )
                        relevance = response.choices[0].message.content.strip()
                        
                        # If Groq indicates a match or relevance, record it
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

if __name__ == "__main__":
    github_token = "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"
    repo_name = "Luthiraa/Go-Fish"
    query = "function to add two numbers"

    results = search_code_with_gpt(query, repo_name, github_token)

    # Print the results
    for result in results:
        print(f"Found in {result['file_path']} at line {result['line_number']}:")
        print(f"Code: {result['code_snippet']}")
        print(f"Groq Relevance: {result['gpt_response']}")
        print("-" * 40)