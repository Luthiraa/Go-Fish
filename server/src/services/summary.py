# import os
# from googleapiclient.discovery import build
# from groq import Groq

# # Load API keys from environment variables
# GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
# GOOGLE_CSE_ID = os.getenv('GOOGLE_CSE_ID')
# GROQ_API_KEY = os.getenv('GROQ_API_KEY')

# # Initialize the Groq client with the API key
# client = Groq(api_key="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")

# def google_search(query, api_key, cse_id, num=5):
#     service = build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=query, cx=cse_id, num=num).execute()
#     return res['items']

# def summarize_text(text):
#     response = client.chat.completions.create(
#         model="llama3-8b-8192",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": f"Summarize the following text in a short paragraph and provide key takeaways:\n\n{text}"}
#         ],
#         max_tokens=150
#     )
#     return response.choices[0].message.content.strip()

# def summarize_search_query(query):
#     search_results = google_search(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
#     summaries = []
#     for result in search_results:
#         title = result.get('title')
#         snippet = result.get('snippet')
#         link = result.get('link')
#         summary = summarize_text(snippet)
#         summaries.append({
#             'title': title,
#             'link': link,
#             'summary': summary
#         })
#     return summaries

# # Example usage
# if __name__ == "__main__":
#     query = "Tell me about ollamma"
#     summaries = summarize_search_query(query)
#     for summary in summaries:
#         print(f"Title: {summary['title']}")
#         print(f"Link: {summary['link']}")
#         print(f"Summary: {summary['summary']}")
#         print("-" * 40)

import os
import requests
from bs4 import BeautifulSoup
from groq import Groq

# Load API keys from environment variables
api_key = "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"

client = Groq(api_key=api_key)

def google_search(query, num=5):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}
    search_url = f"https://www.google.com/search?q={query}&num={num}"
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    search_results = []
    for g in soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd'):
        title = g.get_text()
        link = g.find_parent('a')['href']
        snippet = g.find_next('div', class_='BNeawe s3v9rd AP7Wnd').get_text()
        search_results.append({'title': title, 'link': link, 'snippet': snippet})
        if len(search_results) >= num:
            break
    return search_results


def summarize_text(text):
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Summarize the following text in a short paragraph and provide key takeaways:\n\n{text}"}
        ],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()

def summarize_search_query(query):
    search_results = google_search(query)
    summaries = []
    for result in search_results:
        title = result.get('title')
        snippet = result.get('snippet')
        link = result.get('link')
        summary = summarize_text(snippet)
        summaries.append({
            'title': title,
            'link': link,
            'summary': summary
        })
    return summaries

# Example usage
if __name__ == "__main__":
    query = "Tell me about ollamma"
    summaries = summarize_search_query(query)
    for summary in summaries:
        print(f"Title: {summary['title']}")
        print(f"Link: {summary['link']}")
        print(f"Summary: {summary['summary']}")
        print("-" * 40)