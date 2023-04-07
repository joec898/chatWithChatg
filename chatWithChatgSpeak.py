# -*- coding: utf-8 -*-
"""
chatWithChatgSpeak.py

Created on Sun Apr 3 21:36:12 2023

@author: JC
"""

import time
import sys
import openai
import pyttsx3
from multiprocessing import Process

with open('cg_key.txt', 'r') as key:
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
    {"role": "system", "content": "You’re a kind helpful assistant"}
]


def chat_with_chatgpt(input):
    msges.append({"role": "user", "content": input})
    completion = openai.ChatCompletion.create(
        model=model,
        max_tokens=100,
        messages=msges
    )
    chat_response = completion.choices[0].message.content

    # use the assistant role to store prior responses, which is a ref for answer to a new question
    msges.append({"role": "assistant", "content": chat_response})

    return chat_response


def speak_it(txt):
    speaker.say(txt)
    speaker.runAndWait()


def typing_simulation2(line, addPeriod):
    for r in line:
        sys.stdout.write(r)
        sys.stdout.flush()
        time.sleep(0.005)
    if addPeriod:
        print(".")  # add the period back
    print('', end='\n')


def typing_simulation(line):
    for r in line:
        sys.stdout.write(r)
        sys.stdout.flush()
        time.sleep(0.005)
    print('', end='\n')


def process_response_multprocesses(strings):
    for l in strings:
        p1 = Process(target=speak_it(l))
        p1.start()
        p2 = Process(target=typing_simulation(l))
        p2.start()

        p1.join()
        p2.join()


def process_Response_inlines(strings):
    for l in response:
        if l.find("."):
            l2 = l.split(".")
            # processResponse(l2)
            for l3 in l2:
                if l3:
                    speak_it(l3)
                    typing_simulation(l3, addPeriod=True)
        else:
            speak_it(l)
            typing_simulation(l)


def process_response(strings):
    for l in response:
        speak_it(l)
        typing_simulation(l)


while True:
    prompt = input('\n\nUser: ')
    if prompt == 'done':
        break
    response = chat_with_chatgpt(prompt)

    response = response.split("\n")

    print("Chartgpt: ", end='\n')
    process_response(response)
    # process_response_multprocesses(response)
