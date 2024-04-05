from openai import OpenAI

from decouple import config

client = OpenAI(
    api_key='NA',
    base_url=config("summary_llm")    
)

completion = client.chat.completions.create(
  model=config("summary_model"),
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)