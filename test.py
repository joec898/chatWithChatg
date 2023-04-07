



from gtts import gTTS as gt


txt = "As the moon rises high above,\nAnd the stars twinkle oh so bright,\nOur love seems to grow much stronger,\nOn this perfect romantic night.\n\nYour hand in mine, with a gentle squeeze,\nWe walk along the quiet path,\nAnd whisper sweet nothings to each other,\nAs we bask in each other's warmth.\n\nThe soft breeze plays with your hair,\nAnd your eyes sparkle with delight,\nI am so blessed to have found you,\nMy love, my heart, my life.\n\nThank"
txt = txt.split("\n")
print (txt)

msg = "good monring"

with gt as src:
    gt.gTTS(text=msg, lang='en', slow=True)

