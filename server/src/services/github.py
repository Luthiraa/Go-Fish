import requests
import os
from groq import Groq

# Initialize the Groq API client
api_key = "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"
client = Groq(api_key=api_key)

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

# Function to extract the main keyword from the query using Groq
def extract_keyword(query):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Extract the single most important keyword from the following query, just give me the keyword straight up, ONLY THE KEYWORD, no other text:\n\n{query}"}
        ],
        max_tokens=10
    )
    keyword = response.choices[0].message.content.strip()
    return keyword

# Function to search for code snippets in a GitHub repository
def search_github_code(query, repo, token=None):
    # Extract the main keyword from the query
    keyword = extract_keyword(query)
    if not keyword:
        print("No valid keyword found in the query.")
        return
    
    # Define the GitHub API search URL
    url = "https://api.github.com/search/code"
    
    # Set up query parameters
    search_query = f"{keyword} in:file repo:{repo}"
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
        print(f"Found {results['total_count']} results for '{keyword}' in '{repo}':\n")
        
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
                print(f"No text matches found for '{keyword}' in {file_name}")
    else:
        print(f"Failed to fetch results. Status code: {response.status_code}")
        print(response.json())

# Example usage of the function
if __name__ == "__main__":
    search_query = "find me where summarize_text is"  
    repository = "Luthiraa/Go-Fish" 
    github_token = "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" 
    search_github_code(search_query, repository, github_token)