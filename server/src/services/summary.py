import os
import openai
from googleapiclient.discovery import build
import secrets

GOOGLE_API_KEY = secrets.google_api_key
GOOGLE_CSE_ID = secrets.google_cse_id
OPENAI_API_KEY = secrets.openai_api

openai.api_key = OPENAI_API_KEY

def google_search(query, api_key, cse_id, num=5):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=query, cx=cse_id, num=num).execute()
    return res['items']

def summarize_text(text):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Summarize the following text in a short paragraph and provide key takeaways:\n\n{text}",
        max_tokens=150
    )
    return response.choices[0].text.strip()

def summarize_search_query(query):
    search_results = google_search(query, GOOGLE_API_KEY, GOOGLE_CSE_ID)
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
    query = "OpenAI GPT-3"
    summaries = summarize_search_query(query)
    for summary in summaries:
        print(f"Title: {summary['title']}")
        print(f"Link: {summary['link']}")
        print(f"Summary: {summary['summary']}")
        print("-" * 40)