# -*- coding: utf-8 -*-

import picamera
from time import sleep


def takePhoto():
    camera = picamera.PiCamera()
    camera.start_preview()
    sleep(5) # Camera warm-up time
    camera.capture('./image/sample0.jpg')
    camera.stop_preview()
