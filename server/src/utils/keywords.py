from groq import Groq

api_key = "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"

client = Groq(api_key=api_key)

def generate_keywords(search_terms):
    # Update to use Groq ChatCompletion
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Generate keywords for the following search terms to improve search accuracy:\n\n{search_terms}"}
        ],
        max_tokens=50
    )
    
    keywords = response.choices[0].message.content.strip().split(', ')

    services = ['GitHub', 'Slack', 'Stack Overflow', 'Reddit']
    additional_keywords = {}

    for service in services:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Generate relevant terms for {service} (ONLY IF APPLICABLE) based on the following keywords: {', '.join(keywords)}"}
            ],
            max_tokens=50
        )
        additional_keywords[service.lower()] = response.choices[0].message.content.strip().split(', ')

    return keywords, additional_keywords

if __name__ == "__main__":
    search_terms = "python, machine learning, data analysis"
    keywords, additional_keywords = generate_keywords(search_terms)
    print("Generated Keywords:", keywords)
    print("Additional Keywords:", additional_keywords)