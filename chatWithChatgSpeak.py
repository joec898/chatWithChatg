"""
chatWithChatGpt.py
@ JC Apr 3, 2023
"""

import requests
import time
import sys
import openai
import pyttsx3
from multiprocessing import Process

with open('cg_key.txt','r') as key:
    data = key.read().strip()

api_key = data
openai.api_key = api_key

# init tts speaker
speaker = pyttsx3.init()
speaker.setProperty('rate', 125)
voices = speaker.getProperty('voices')
# voices index, 1 for female (0 for male)
speaker.setProperty('voice', voices[1].id)

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

def speak_it(txt):
    speaker.say(txt)
    speaker.runAndWait()

def typing_simulation(line, addPeriod):
    for r in line:
        sys.stdout.write(r)
        sys.stdout.flush()
        time.sleep(0.005)
    if addPeriod:
        print(".") # add the period back
    print('', end='\n')

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

def processResponseMultProcesses(strings):
    for l in strings:
        p1 = Process(target = speak_it(l) )
        p1.start()
        p2 = Process(target = typing_simulation(l))
        p2.start()

        p1.join()
        p2.join()

def processResponse(strings):
    for l in response:
        if l.find("."):
            l2 = l.split(".")
            #processResponse(l2)
            for l3 in l2:
                if l3:
                    speak_it(l3)
                    typing_simulation(l3, addPeriod=True)
        else:
            speak_it(l)
            typing_simulation(l)

while True:
    prompt = input('\n\nUser: ')
    if prompt == 'done':
        break
    response = chat_with_chatgpt(prompt)

    response = response.split("\n")

    print("Chartgpt: ", end='\n')
    processResponse(response)
    #processResponseMultProcesses(response)

