# -*- coding: utf-8 -*-
import sys
import cv2
import numpy as np
import imutils
import ocr
from object_detection import objectdetection
from ocr import get_credentials, ocr
from takePhoto import takephoto
from laplacian import variance_of_laplacian, notblurry
from audio import command, getContent, outcome
from matplotlib import pyplot
from scipy.stats import gaussian_kde


def run():
    #print(command)
    c = command()
    if c == "閱讀" or c == "閱讀模式":
        takephoto()
        notblurry()
        ocr()
        outcome('./result/audio/outcome.txt')
    elif c == "用餐" or c == "用餐模式":
        takephoto()
        objectdetection()
        outcome('./result/audio/objoutcome.txt')
    elif c == "沒事" or c == "結束":
        return 0
    else:
        outcome('./result/audio/responsenoidea.txt')



if __name__ == '__main__':
    while(1):
        print("[INFO] 請選擇模式")
        #command()
        run()



#GOOGLE_TTS_URL = 'https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=zh-TW&q=' + content
#getMP3(GOOGLE_TTS_URL)
#playMP3()
