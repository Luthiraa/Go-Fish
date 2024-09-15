import requests
import re
import argparse

repo_link = "https://github.com/Luthiraa/Go-Fish"
keywords = ["function", "add", "two", "numbers"]


def search_github_repo(repo_link, keywords):
    # Extract owner and repo name from the link
    repo_path = repo_link.replace("https://github.com/", "")
    api_url = f"https://api.github.com/repos/{repo_path}/contents"
    
    # Fetch repository contents
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repository contents: {response.status_code}")
    
    repo_contents = response.json()
    matching_snippets = []

    # Define a function to search for keywords in a file
    def search_file(file_url):
        file_response = requests.get(file_url)
        if file_response.status_code != 200:
            return []
        
        file_content = file_response.text
        snippets = []
        for keyword in keywords:
            matches = re.findall(rf".*{keyword}.*", file_content, re.IGNORECASE)
            snippets.extend(matches)
        return snippets

    # Iterate through the files in the repository
    for item in repo_contents:
        if item['type'] == 'file':
            file_url = item['download_url']
            snippets = search_file(file_url)
            if snippets:
                matching_snippets.append({
                    'file': item['path'],
                    'snippets': snippets
                })
    
    return matching_snippets

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search a GitHub repository for code snippets matching keywords.")
    parser.add_argument("repo_link", type=str, help="The GitHub repository link")
    parser.add_argument("keywords", type=str, nargs='+', help="Keywords to search for in the repository")

    args = parser.parse_args()
    repo_link = args.repo_link
    keywords = args.keywords

    results = search_github_repo(repo_link, keywords)
    
    for result in results:
        print(f"File: {result['file']}")
        for snippet in result['snippets']:
            print(f"  {snippet}")