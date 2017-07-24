import os
from pygame import mixer
import datetime
from time import sleep
from _thread import exit
from gtts import gTTS


def tts(message):
    now_time = datetime.datetime.now()
    mp3_nameold = '111'
    mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"

    mixer.init()
    print(message)
    tts = gTTS(text=message, lang='ru')
    tts.save('tts/' + mp3_name)
    mixer.music.load('tts/' + mp3_name)
    mixer.music.play()
    while mixer.music.get_busy():
        sleep(0.1)
    mp3_nameold = mp3_name
    mixer.music.load('tts/1.mp3')
    mixer.stop
    mixer.quit
    if (os.path.exists('tts/' + mp3_nameold)):
        os.remove('tts/' + mp3_nameold)
    if (os.path.exists('tts/' + mp3_name)):
        os.remove('tts/' + mp3_name)
    exit()