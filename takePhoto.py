# -*- coding: utf-8 -*-
import cv2
import numpy as np


def takephoto():
    # takephoto
    cap = cv2.VideoCapture(0) # Generate camera object
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1) # turn the autofocus on
    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("./origin/takephoto.png", frame)
            break
    cap.release()
    cv2.destroyAllWindows()

def objectphoto():
    # takephoto
    cap = cv2.VideoCapture(0) # Generate camera object
    cap.set(3,1280)
    cap.set(4,720)
    cap.set(cv2.CAP_PROP_AUTOFOCUS, 1) # turn the autofocus on
    while(1):
        # get a frame
        ret, frame = cap.read()
        # show a frame
        cv2.imshow("capture", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("./origin/object.png", frame)
            break
    cap.release()
    cv2.destroyAllWindows()

#takephoto()
#notblurry()




