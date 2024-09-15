import requests
import os
from groq import Groq

# Initialize the Groq API client
api_key = "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"
client = Groq(api_key=api_key)

# Function to extract the main keyword from the query using Groq
def extract_keyword(query):
    try:
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
    except Exception as e:
        print(f"Error extracting keyword: {str(e)}")
        return None

# Function to search for code snippets in a GitHub repository
def search_github_code(query, repo, token=None):
    # Extract the main keyword from the query
    keyword = extract_keyword(query)
    if not keyword:
        print("No valid keyword found in the query.")
        return None, None, None
    
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
    
    # Print the request details for debugging
    print(f"Sending request to GitHub API: {url}")
    print(f"Headers: {headers}")
    print(f"Params: {params}")
    
    try:
        # Send GET request to GitHub Search API
        response = requests.get(url, headers=headers, params=params)
        
        # Print the response status code and headers for debugging
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        # Initialize variables to store the top result
        top_url = None
        top_line_number = None
        top_snippet = None
        
        # Check if the request was successful
        if response.status_code == 200:
            results = response.json()
            print(f"Found {results['total_count']} results for '{keyword}' in '{repo}':\n")
            
            # Process only the top search result
            if results['items']:
                top_result = results['items'][0]
                top_url = top_result['html_url']
                print(f"Fetching code from: {top_url}")
                
                # Extract the matching lines from the top result
                if 'text_matches' in top_result:
                    top_snippet = top_result['text_matches'][0]['fragment']
                    top_line_number = top_result['text_matches'][0]['matches'][0]['indices'][0] + 1
                else:
                    print(f"No text matches found for '{keyword}' in {top_result['name']}")
            else:
                print(f"No results found for '{keyword}' in '{repo}'")
        else:
            print(f"Failed to fetch results. Status code: {response.status_code}")
            print(response.json())
        
        return top_url, top_line_number, top_snippet
    except Exception as e:
        print(f"Error during GitHub search: {str(e)}")
        return None, None, None

# Example usage of the function
if __name__ == "__main__":
    search_query = "find me where summarize_text is"  # The code snippet or term you're searching for
    repository = "Luthiraa/Go-Fish"  # GitHub repository in "owner/repo" format
    github_token = "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"  # Get GitHub Personal Access Token from environment variable
    
    if not github_token:
        print("GitHub token not found. Please set the GITHUB_TOKEN environment variable.")
    else:
        # Call the search function
        top_url, top_line_number, top_snippet = search_github_code(search_query, repository, github_token)
        
        # Print the top result
        print("URL:", top_url)
        print("Top Line Number:", top_line_number)
        print("Top Snippet:", top_snippet)
