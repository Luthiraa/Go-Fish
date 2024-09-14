from groq import Groq

# Set your Groq API key directly in the script
api_key = "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"

# Initialize the Groq client with the API key
client = Groq(api_key=api_key)

# Create a chat completion request
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain the importance of fast language models",
        }
    ],
    model="llama3-8b-8192",
)

# Print the response
print(chat_completion.choices[0].message.content)