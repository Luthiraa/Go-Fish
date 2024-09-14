from openai import OpenAI
import os

os.environ['OPENAI_API_KEY'] = "sk-Fwq1VJvvpMNHb_2d18fC9_bdcT66f2doBp7c-DoP_ST3BlbkFJ2qfIaxsmZblPx6FR_ZKaPKiiOrCu46nlHz5K1-BysA"

client = OpenAI()

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Generate me 3 Jargons that I can use for my Social Media content as a Data Scientist content creator"}
  ]
)

print(completion.choices[0].message.content)