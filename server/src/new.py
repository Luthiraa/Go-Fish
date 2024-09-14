from googlesearch import search
import requests
from bs4 import BeautifulSoup

# Step 1: Get the top 5 search results from Google
def get_top_google_results(query, num_results=5):
    search_results = []
    for result in search(query, num=num_results, stop=num_results):
        search_results.append(result)
    return search_results

# Step 2: Parse and extract text from a web page
def extract_text_from_url(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract visible text (you can improve this extraction depending on the website structure)
        texts = soup.findAll(text=True)
        visible_texts = filter(tag_visible, texts)
        return u" ".join(t.strip() for t in visible_texts)
    except Exception as e:
        print(f"Failed to fetch content from {url}: {e}")
        return None

# Helper function to filter visible text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

# Step 3: Summarize the text using the Groq API (replace with actual API URL)
def summarize_text_with_groq(text):
    groq_api_url = "https://api.groq.com/summarize"  # Replace with actual API endpoint
    headers = {"Content-Type": "application/json"}
    payload = {
        "text": text,
        "summary_length": "short"  # Adjust as needed
    }
    try:
        response = requests.post(groq_api_url, json=payload, headers=headers)
        summary = response.json().get("summary")
        return summary
    except Exception as e:
        print(f"Failed to summarize text: {e}")
        return None

# Step 4: Main function to run the search and summarization process
def main():
    query = input("Enter search query: ")
    
    # Get top 5 search results
    search_results = get_top_google_results(query)
    print(f"Top {len(search_results)} search results fetched.")
    
    # Process each result
    for index, url in enumerate(search_results):
        print(f"\nFetching and summarizing content from: {url}")
        text_content = extract_text_from_url(url)
        if text_content:
            summary = summarize_text_with_groq(text_content)
            if summary:
                print(f"Summary {index + 1}: {summary}")
            else:
                print("Could not generate summary.")
        else:
            print("No text content to summarize.")

if __name__ == "__main__":
    main()
