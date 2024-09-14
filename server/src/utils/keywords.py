import openai
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_keywords(search_terms):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Generate keywords for the following search terms to improve search accuracy:\n\n{search_terms}",
        max_tokens=50
    )
    keywords = response.choices[0].text.strip().split(', ')

    services = ['GitHub', 'Slack', 'Stack Overflow', 'Reddit']
    additional_keywords = {}

    for service in services:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Generate relevant terms for {service} ONLY IF APPLICABLE based on the following keywords: {', '.join(keywords)}",
            max_tokens=50
        )
        additional_keywords[service.lower()] = response.choices[0].text.strip().split(', ')

    return keywords, additional_keywords

if __name__ == "__main__":
    search_terms = "python, machine learning, data analysis"
    keywords, additional_keywords = generate_keywords(search_terms)
    print("Generated Keywords:", keywords)
    print("Additional Keywords:", additional_keywords)