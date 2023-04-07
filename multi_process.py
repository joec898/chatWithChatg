# -*- coding: utf-8 -*-
"""
chatWithPyChatGPT.py

Created on Sun Apr 6, 2023 21:05:41 2023

@author: JC
"""

import time
import sys

import pyttsx3
import threading
from multiprocessing import Process
from multiprocessing import Pool

def init_engine():
    speaker = pyttsx3.init()
    speaker.setProperty('rate', 125)
    voices = speaker.getProperty('voices')
    # voices index, 1 for female (0 for male)
    speaker.setProperty('voice', voices[1].id)
    return speaker

messages = ['As the moon rises high above, and the stars twinkle oh so bright,',
            'Our love seems to grow much stronger,',
            'On this perfect romantic night.',
            'Your hand in mine, with a gentle squeeze,',
            'We walk along the quiet path,',
            'And whisper sweet nothings to each other,',
            "As we bask in each other's warmth.",
            'The soft breeze plays with your hair,',
            'And your eyes sparkle with delight,',
            'I am so blessed to have found you,',
            'My love, my heart, my life.']

def speak_it(txt):
    speaker = init_engine()
    speaker.say(txt)
    speaker.runAndWait()
    speaker.stop()
    speaker = None

def typing_simulation(line):
    for r in line:
        sys.stdout.write(r)
        sys.stdout.flush()
        time.sleep(0.05)
    print('', end='\n')

def print_vocalize(phrase):
    speak_it(phrase)
    #print(l)
    typing_simulation(phrase)
    time.sleep(0.1)

def print_vocalize_thread(phrase):
    t = threading.Thread(target=speak_it, args=(phrase,))
    t.start()
    typing_simulation(l)

def print_vocalize_multiprocess(phrase):
    p = Process(target=speak_it, args=(phrase,))
    p2 = Process(target=typing_simulation, args=(phrase,))
    p.run()
    p2.run()

def print_vocalize_pool(phrase):
    pool = Pool()
    pool.apply_async(speak_it, args = (phrase, ),)
    #pool.apply_async(typing_simulation, args = (phrase, ),)
    typing_simulation(l)
    pool.close()
    pool.join()

print("Start vocolizing...")
for l in messages:
    print_vocalize_pool(l)

print("Ended vocolizing.")
