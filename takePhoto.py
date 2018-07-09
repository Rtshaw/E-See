# -*- coding: utf-8 -*-

import picamera
import time


def takePhoto():
    camera = picamera.PiCamera()
    time.sleep(2) # Camera warm-up time
    camera.capture('./image/sample0.jpg')
