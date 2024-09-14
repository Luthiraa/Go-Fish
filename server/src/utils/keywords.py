import openai
import os

# Set the OpenAI API key
# openai.api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = "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"
def generate_keywords(search_terms):
    # Update to use ChatCompletion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate keywords for the following search terms to improve search accuracy:\n\n{search_terms}"}
        ],
        max_tokens=50
    )
    
    keywords = response['choices'][0]['message']['content'].strip().split(', ')

    services = ['GitHub', 'Slack', 'Stack Overflow', 'Reddit']
    additional_keywords = {}

    for service in services:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate relevant terms for {service} (ONLY IF APPLICABLE) based on the following keywords: {', '.join(keywords)}"}
            ],
            max_tokens=50
        )
        additional_keywords[service.lower()] = response['choices'][0]['message']['content'].strip().split(', ')

    return keywords, additional_keywords

if __name__ == "__main__":
    search_terms = "python, machine learning, data analysis"
    keywords, additional_keywords = generate_keywords(search_terms)
    print("Generated Keywords:", keywords)
    print("Additional Keywords:", additional_keywords)
