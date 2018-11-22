# -*- coding: utf-8 -*-
# import the necessary packages
import os
import speech_recognition
import tempfile
from gtts import gTTS
from pygame import mixer, display, time, event



# voice to word
def command():
    r = speech_recognition.Recognizer()

    with speech_recognition.Microphone() as source:
        print("[INFO] Start speeking.")
        audio = r.listen(source)

    text = r.recognize_google(audio, language='zh-TW')
    #print(text)

    if os.path.exists('./result/audio/'):
        print("[INFO] ..OK")
    else:
        print("[INFO] audio directory is not exist, now create it.")
        os.mkdir('./result/audio/')
        print("[INFO] ..OK")


    if os.path.isfile('./result/audio/command.txt'):
        with open('./result/audio/command.txt', 'w') as f:
            f.write('%s' %text)
    else:
        with open('./result/audio/command.txt', 'w') as f:
            f.write('%s' %text)

    print("[INFO] command.txt is created success.")
    return text


def getContent(txtfile):
    # 讀 output.txt
    with open(txtfile, encoding = 'utf-8-sig') as f:
        content = f.read().strip()
        content = content.replace('________________', '')
        #print(content)
    return content

# txt's word to voice
def outcome(txtfile):
    
    
    if os.path.isfile(txtfile):
        word = getContent(txtfile)
        #print(word)
        """
        with open(txtfile, 'r') as f:
            word = f.read()
            #print(word)
            """
    else:
        print("[INFO] 圖像無法識別請於提示音後重新操作.")

    with tempfile.NamedTemporaryFile(delete=True) as fp:
        tts = gTTS(text=word, lang='zh-TW')
        tts.save('./result/audio/outcome.mp3')
        mixer.init()
        mixer.music.load('./result/audio/outcome.mp3')
        print("[INFO] Start play outcome.")
        screen=display.set_mode([200,50])
        mixer.music.play(0)
        clock = time.Clock()
        clock.tick(10)
    while mixer.music.get_busy():
        event.poll()
        clock.tick(10)

#command()
#outcome('../../E-See/tmp.txt')
