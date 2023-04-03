"""
chatWithChatGpt.py
@ JC Apr 3, 2023
"""

import requests
import time
import sys
import openai

with open('cg_key.txt','r') as key:
    data = key.read().strip()

api_key = data
openai.api_key = api_key

model = 'gpt-3.5-turbo'  
msges = [
 {"role": "system", "content" : "You’re a kind helpful assistant"}
]

def chat_with_chatgpt(input):
    msges.append({"role":"user", "content": input})
    completion = openai.ChatCompletion.create(
        model = model,
        max_tokens = 100,
        messages=msges
    )
    chat_response = completion.choices[0].message.content

    # use the assistant role to store prior responses, which is a ref for answer to a new question 
    msges.append({"role": "assistant", "content": chat_response})

    return chat_response

def chat_with_chatgpt_url(input):
    res = requests.post(f"https://api.openai.com/v1/completions",
                        headers= {
                            "Content-Type": "application/json",
                            "Authorization": f"Bearer {api_key}"
                        },
                        json={
                            "model": model,
                            "prompt": input,
                            "max_tokens": 100,
                            "instruction": "Fix the spelling mistakes" 
                        }).json()
    return res['choices'][0]['text']

while True:
    prompt = input('\n\nUser: ')
    if prompt == 'done':
        break
    response = chat_with_chatgpt(prompt)

    # simulating chatGpt printing
    print("Chartgpt: ", end='\n')
    for r in response:
        sys.stdout.write(r)
        sys.stdout.flush()
        time.sleep(0.01)    
