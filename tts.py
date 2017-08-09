import datetime
import os
from _thread import exit
from time import sleep
from gtts import gTTS
from yandex_speech import TTS
from pygame import mixer

import config


def googletts(message):
    now_time = datetime.datetime.now()
    mp3_nameold = '111'
    mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"

    mixer.init()
    print('### SPEECH MSG: ' + message)
    tts = gTTS(text=message, lang='ru')
    tts.save('gtts/' + mp3_name)
    mixer.music.load('gtts/' + mp3_name)
    mixer.music.play()
    while mixer.music.get_busy():
        sleep(0.1)
    mp3_nameold = mp3_name
    mixer.music.load('gtts/1.mp3')
#    mixer.stop
#    mixer.quit
    if (os.path.exists('gtts/' + mp3_nameold)):
        os.remove('gtts/' + mp3_nameold)
    if (os.path.exists('gtts/' + mp3_name)):
        os.remove('gtts/' + mp3_name)
    exit()


def yandextts(message):
    now_time = datetime.datetime.now()
    mp3_nameold = '111'
    mp3_name = now_time.strftime("%d%m%Y%I%M%S") + ".mp3"

    mixer.init()
    print('### SPEECH MSG: ' + message)
    speech = TTS(config.speaker, config.audio_format, config.key)
    speech.generate(message)
    speech.save('ytts/' + mp3_name)
    mixer.music.load('ytts/' + mp3_name)
    mixer.music.play()
    while mixer.music.get_busy():
        sleep(0.1)
    mp3_nameold = mp3_name
    mixer.music.load('ytts/1.mp3')
#    mixer.stop
#    mixer.quit
    if (os.path.exists('ytts/' + mp3_nameold)):
        os.remove('ytts/' + mp3_nameold)
    if (os.path.exists('ytts/' + mp3_name)):
        os.remove('ytts/' + mp3_name)
    exit()