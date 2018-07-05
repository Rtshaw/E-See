# -*- coding: utf-8 -*-

import picamera
from time import sleep

camera = picamera.PiCamera()
time.sleep(2) # Camera warm-up time
camera.capture('test.jpg')