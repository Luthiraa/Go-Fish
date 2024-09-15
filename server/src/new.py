import requests
import os

# Function to save the snippet to a text file
def save_snippet_to_file(file_name, snippet, query, line_number, file_url):
    # Create a directory for the snippets if it doesn't exist
    if not os.path.exists('snippets'):
        os.makedirs('snippets')
    
    # Save the snippet to a text file
    with open(f'snippets/{file_name}.txt', 'w') as f:
        f.write(f"First occurrence at line: {line_number}\n")
        f.write(f"URL: {file_url}\n\n")
        f.write(snippet)

    print(f"Snippet saved to snippets/{file_name}.txt")

# Function to search for code snippets in a GitHub repository
def search_github_code(query, repo, token=None):
    # Define the GitHub API search URL
    url = "https://api.github.com/search/code"
    
    # Set up query parameters
    search_query = f"{query} in:file repo:{repo}"
    params = {
        'q': search_query
    }
    headers = {
        "Accept": "application/vnd.github.v3.text-match+json"
    }
    if token:
        headers["Authorization"] = f"token {token}"
    
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
            
            # Extract the matching lines from the search result
            if 'text_matches' in item:
                snippet = item['text_matches'][0]['fragment']
                line_number = item['text_matches'][0]['matches'][0]['indices'][0] + 1
                # Save the snippet to a text file
                save_snippet_to_file(file_name, snippet, query, line_number, file_url)
            else:
                print(f"No text matches found for '{query}' in {file_name}")
    else:
        print(f"Failed to fetch results. Status code: {response.status_code}")
        print(response.json())

# Example usage of the function
if __name__ == "__main__":
    search_query = "summarize_text"  # The code snippet or term you're searching for
    repository = "Luthiraa/Go-Fish"  # GitHub repository in "owner/repo" format
    github_token = "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"  # GitHub Personal Access Token
    
    # Call the search function
    search_github_code(search_query, repository, github_token)