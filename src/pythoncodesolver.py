import os
from random import choices
from secrets import choice
from click import prompt
from matplotlib.pyplot import text
import openai

openai.api_key = "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"

prompt = input("enter your question ")

response = openai.Completion.create(
  engine="text-davinci-002",
  prompt=prompt,
  temperature=0,
  max_tokens=60,
  top_p=1.0,
  frequency_penalty=0.0,
  presence_penalty=0.0
)

for i in response['choices']:
    print(i['text'])