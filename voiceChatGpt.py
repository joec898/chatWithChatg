# -*- coding: utf-8 -*-
"""
voiceChatGpt.py

Created on Mon Apr 4, 2023 10:20:41 2023

@author: JC
"""

import time
import sys
import openai
import pyttsx3
import speech_recognition as sr
import asyncio

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

# Init recognizer
rec = sr.Recognizer()
mic = sr.Microphe()
#mic = sr.Microphone(device_index=1)

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

    # use the assistant role to store prev responses, which serves a ref for answer to next question
    msges.append({"role": "assistant", "content": chat_response})

    return chat_response


def speak_it(txt):
    speaker.say(txt)
    speaker.runAndWait()
    print(txt)


def typing_simulation(line):
    for r in line:
        sys.stdout.write(r)
        sys.stdout.flush()
        time.sleep(0.005)
    print('', end='\n')


async def voice_input():
    audio = None
    txt = None
    with mic as src:
        rec.adjust_for_ambient_noise(src, duration=0.2)

        #r.adjust_for_ambient_noise(src)
        while audio == None:
            audio = rec.listen(src)

        if audio != None:
            try:
                txt = rec.recognize_google(audio)
                txt = txt.lower()
            except Exception as e:
                print("Oops! Something goes wrong: " + e)
            finally:
                txt = None
        return txt

while True:
    print("Speak to your microphone with your question.")
    txt = asyncio.run(voice_input())
    #print(f"txt = [{txt}].")

    if txt != None:
        print("You said: ", txt)
        if txt == 'i am done' or txt == "i'am done" or txt == 'done':
            speak_it("Good bye")
            txt = None
            quit()

        response = chat_with_chatgpt(txt)
        response = response.split("\n")
        print("Chartgpt: ", end='\n')
        for l in response:
            speak_it(l)
            #print(l)
            # typing_simulation(l)
        txt = None

    #print('', end='\n')
