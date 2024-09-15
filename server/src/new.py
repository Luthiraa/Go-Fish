import requests
import os

# Function to fetch the raw file content from GitHub
def fetch_raw_file_content(file_url):
    # Convert the GitHub URL to raw content URL
    raw_url = file_url.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    
    # Fetch the raw file content
    response = requests.get(raw_url)
    
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to fetch file content. Status code: {response.status_code}")
        return None

# Function to save the snippet to a text file
def save_snippet_to_file(file_name, snippet, query):
    # Create a directory for the snippets if it doesn't exist
    if not os.path.exists('snippets'):
        os.makedirs('snippets')
    
    # Save the snippet to a text file
    with open(f'snippets/{file_name}.txt', 'w') as f:
        f.write(f"Code snippet for search query: {query}\n\n")
        f.write(snippet)

    print(f"Snippet saved to snippets/{file_name}.txt")

# Function to search for code snippets in a GitHub repository
def search_github_code(query, language, repo, token=None):
    # Define the GitHub API search URL
    url = "https://api.github.com/search/code"
    
    # Set up query parameters
    search_query = f"{query} in:file language:{language} repo:{repo}"
    params = {
        'q': search_query
    }
    
    # Headers for the request, including authorization if a token is provided
    headers = {}
    if token:
        headers = {
            "Authorization": f"token {token}"
        }
    
    # Send GET request to GitHub Search API
    response = requests.get(url, headers=headers, params=params)
    
    # Check if the request was successful
    if response.status_code == 200:
        results = response.json()
        print(f"Found {results['total_count']} results for '{query}' in '{repo}':\n")
        
        # Loop through each search result and fetch the code snippet
        for item in results['items']:
            file_name = item['name']
            file_url = item['html_url']
            print(f"Fetching code from: {file_url}")
            
            # Fetch the raw content of the file
            raw_content = fetch_raw_file_content(file_url)
            
            if raw_content:
                # Check if the query is present in the file content
                lines = raw_content.splitlines()
                snippet_lines = [line for line in lines if query in line]
                snippet = "\n".join(snippet_lines)
                
                if snippet:
                    # Save the snippet to a text file
                    save_snippet_to_file(file_name, snippet, query)
                else:
                    print(f"No code snippet found for '{query}' in {file_name}")
    else:
        print(f"Failed to fetch results. Status code: {response.status_code}")
        print(response.json())

# Example usage of the function
if __name__ == "__main__":
    search_query = "summarize_text"  # The code snippet or term you're searching for
    programming_language = "python"  # Programming language
    repository = "Luthiraa/Go-Fish"  # GitHub repository in "owner/repo" format
    github_token = "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"  # GitHub Personal Access Token
    
    # Call the search function
    search_github_code(search_query, programming_language, repository, github_token)
