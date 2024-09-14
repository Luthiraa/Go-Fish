const fetch = require('node-fetch');

// Set your OpenAI API key
const apiKey = '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"';

async function getSimilarAnimals() {
  const url = 'https://api.openai.com/v1/chat/completions';

  // Prepare the API request
  const response = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${apiKey}`
    },
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: [
        { role: 'system', content: 'You are a helpful assistant.' },
        { role: 'user', content: 'Name 5 animals similar to bears.' }
      ],
      max_tokens: 50
    })
  });

  const data = await response.json();
  // Extract and return the response
  const answer = data.choices[0].message.content.trim();
  return answer;
}

// Run the function
getSimilarAnimals().then(result => {
  console.log("Animals similar to bears:", result);
}).catch(error => {
  console.error("Error:", error);
});
