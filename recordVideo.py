# -*-coding: utf-8 -*-

import picamera
camera = picamera.PiCamera()
camera.start_recording('video.h264')
camera.wait_recording(3)
camera.stop_recording()
