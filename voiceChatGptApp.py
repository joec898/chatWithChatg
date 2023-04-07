# -*- coding: utf-8 -*-
"""
voiceChatGptApp.py

Created on Mon Apr 5, 2023 20:55:41 2023

@author: JC
"""

import time
import sys
import openai as ai
import pyttsx3
import speech_recognition as sr
import asyncio

def main():
    with open('cg_key.txt', 'r') as key:
        data = key.read().strip()
        api_key = data

    vcg = voice_chat_gpt(api_key)
    vcg.voice_chat()


class voice_chat_gpt:
    def __init__(self, api_key) -> None:
        ai.api_key = api_key

    def voice_chat(self):
        # init tts speaker
        speaker = pyttsx3.init()
        speaker.setProperty('rate', 125)
        voices = speaker.getProperty('voices')
        # voices index, 1 for female (0 for male)
        speaker.setProperty('voice', voices[1].id)

        # Init recognizer
        rec = sr.Recognizer()
        mic = None
        mic = sr.Microphone()
        #mic = sr.Microphone(device_index=1)

        model = 'gpt-3.5-turbo'
        contents = [
            {"role": "system", "content": "You’re a kind helpful assistant"}
        ]

        while True:
            print("Speak to your microphone with your question.")

            message = self.voice_input(rec, mic)
            #print(f"txt = [{txt}].")

            if message != None:
                message = message.lower()
                print("You said: ", txt)
                if message == 'i am done' or message == "i'am done" or message == 'done':
                    self.speak_it("Good bye")
                    txt = None
                    quit()

                response = self.chat_with_chatgpt(contents, model, message)
                response = response.split("\n")
                print("Chartgpt: ", end='\n')
                for l in response:
                    self.print_vocalize(speaker, l)

                txt = None

            #print('', end='\n')

    def chat_with_chatgpt(self, contents, model, input):
        contents.append({"role": "user", "content": input})
        completion = ai.ChatCompletion.create(
            model=model,
            max_tokens=100,
            messages=contents
        )
        chat_response = completion.choices[0].message.content

        # use the assistant role to store prev responses, which serves a ref for answer to next question
        contents.append({"role": "assistant", "content": chat_response})

        return chat_response

    def print_vocalize(self, speaker, phrase):
        speaker.say(phrase)
        speaker.runAndWait()
        print(phrase)

    def typing_simulation(self, line):
        for r in line:
            sys.stdout.write(r)
            sys.stdout.flush()
            time.sleep(0.005)
        print('', end='\n')

    def voice_input(self, recognizer, mic):
        audio = None
        txt = None
        with mic as src:
        #with sr.Microphone() as src:
            recognizer.adjust_for_ambient_noise(src, duration=0.2)

            # r.adjust_for_ambient_noise(src)
            while audio == None:
                audio = recognizer.listen(src)

            if audio != None:
                try:
                    txt = recognizer.recognize_google(audio)
                except Exception as e:
                    print("Oops! Something goes wrong: " + e)

        return txt

def test():
    main()

#if __name__ == "__main__":
#    main()

test()
