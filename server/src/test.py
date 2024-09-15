import requests
import json

def search_github_repo(query, repo, language=None, max_results=5):
    # Define the GitHub API URL for searching code
    api_url = 'https://api.github.com/search/code'
    
    # Create the query parameters
    search_query = f'{query}+repo:{repo}'
    if language:
        search_query += f'+language:{language}'
    
    # Set the parameters
    params = {
        'q': search_query,
        'per_page': max_results
    }
    
    # Make the request to the GitHub API
    response = requests.get(api_url, params=params)
    
    # Check for successful response
    if response.status_code == 200:
        # Parse the JSON response
        results = response.json()['items']
        if results:
            print(f'Found {len(results)} code snippets:')
            for idx, result in enumerate(results, 1):
                # Fetch the actual content of the file
                file_url = result['html_url']
                raw_url = file_url.replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                file_response = requests.get(raw_url)
                
                if file_response.status_code == 200:
                    print(f"\nSnippet {idx} - File: {result['name']} (Repo: {result['repository']['full_name']})")
                    print(f"URL: {file_url}")
                    print("\n```")
                    print(file_response.text[:500])  # Display the first 500 characters of the file
                    print("```")
                else:
                    print(f"Could not fetch content for {result['name']}.")
        else:
            print('No code snippets found.')
    else:
        print(f'Error: {response.status_code} - {response.text}')

# Example usage
if __name__ == "__main__":
    search_query = input("Enter your search query: ")
    repository = input("Enter the GitHub repository (owner/repo): ")
    language = input("Enter the programming language (optional): ")
    search_github_repo(search_query, repository, language)
