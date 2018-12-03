# -*- coding: utf-8 -*-
# import the necessary packages
import os
import cv2
import sys
import time
import audio
import speech_recognition
from ocr import get_credentials, ocr
from object_detection import objectdetection
from audio import outcome, getContent
from PyQt5.QtMultimedia import QSound
from PyQt5.QtGui import QPixmap, QFont, QImage
from PyQt5.QtCore import QTimer, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QVBoxLayout,  QTextEdit, QWidget, QLabel, QGraphicsView, QGraphicsScene, QHBoxLayout
from PyQt5 import QtCore, QtWidgets


### window 1
class AudioUi(QWidget):
    
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.wavplay()
    
    def initUI(self):
        self.setWindowTitle("AudioUi")
        
        layout = QtWidgets.QGridLayout()
        
        self.resize(250, 150)
        self.move(300, 300)
        self.text = QLabel("請選擇模式", self)
        self.text.setGeometry(90, 50, 150 ,30)
        
        self.button = QtWidgets.QPushButton('Next')
        
        self.button.clicked.connect(self.switch)
        
        layout.addWidget(self.button)
        
        self.setLayout(layout)
    
        #self.show()
    
    def switch(self):
        self.switch_window.emit()

    def wavplay(self):
        self.sound = QSound('./origin/choosemode.wav')
        self.sound.play()


### window 2
class CommandUi(QWidget):
    
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.wavplay()

    def initUI(self):
        self.setWindowTitle("CommandUi")
        
        layout = QtWidgets.QGridLayout()
        
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)
        
        self.button = QtWidgets.QPushButton('Command')
        self.button.clicked.connect(self.command)
        
        #self.button2 = QtWidgets.QPushButton('Next')
        #self.button2.clicked.connect(self.switch)
        
        
        layout.addWidget(self.button)
        #layout.addWidget(self.button2)
        
        self.setLayout(layout)
        
        self.resize(250, 150)
        self.move(300, 300)
        pic = QPixmap('./origin/volume.png')
        self.lb = QLabel(self)
        self.lb.setGeometry(50, 50, 150, 30)
        self.lb.setPixmap(pic)


    def wavplay(self):
        self.sound = QSound('./origin/instruction.wav')
        self.sound.play()
    
    def command(self):
        self.switch_window.emit()
        
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



#self.show()

def getCameraNum():
    """獲取攝像頭數量"""
    num = 0
    for i in range(0,5):
        # 從攝像頭中取得視訊
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            num =1
            cap.release()
    return num

class FrameThread(QThread):
    imgLab = None
    device = None
    paizhao = 0
    """攝像頭拍照執行緒，攝像頭拍照耗時較長容易卡住UI"""
    
    def __init__(self, deviceIndex, imgLab):
        QThread.__init__(self)
        self.imgLab = imgLab
        self.deviceIndex = deviceIndex
        self.device = cv2.VideoCapture(self.deviceIndex)  # 從攝像頭中取得視訊
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    
    def run(self):
        if self.device.isOpened():
            try:
                while True:
                    ret, frame = self.device.read()
                    height, width, bytesPerComponent = frame.shape
                    bytesPerLine = bytesPerComponent * width
                    # 變換彩色空間順序
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                    # 轉為QImage物件
                    image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                    if self.paizhao == 1:
                        image.save('./origin/takephoto.png')
                        self.paizhao = 0
                        pixmap = QPixmap.fromImage(image)
                        pixmap = pixmap.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
                        self.imgLab.setPixmap(pixmap)
                        ocr()
                        outcome('./result/audio/outcome.txt')
            finally:
                self.device.release()

    def destroyed(self, QObject=None):
        self.device.release()

    def switch(self):
        self.switch_window.emit()


### window 3.1
class MainWindow(QWidget):
    
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self, camera_index=0, fps=30):
        super().__init__()
        
        self.capture = cv2.VideoCapture(camera_index)
        self.dimensions = self.capture.read()[1].shape[1::-1]
        
        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)
        
        view = QGraphicsView(self)
        view.setScene(scene)
        
        text = QLabel('準備就緒', self)
        text.move(50, 575)
        
        layout = QVBoxLayout(self)
        layout.addWidget(view)
        #layout.addWidget(text)
        
        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()
        
        self.initUI()
    
    def initUI(self):
        hbox = QHBoxLayout(self)
        
        lb1 = QLabel(self)
        lb2 = QLabel(self)
        
        btn = QPushButton(self)
        btn.setText("拍照")
        btn.move(800, 530)
        btn.clicked.connect(self.paizhao)
        
        btn2 = QPushButton(self)
        btn2.setText("Next")
        btn2.move(800, 500)
        btn2.clicked.connect(self.switch)
        
        self.frameThread = FrameThread(0,lb1)
        self.frameThread.start()
        self.frameThread2 = FrameThread(1,lb2)
        self.frameThread2.start()
        
        hbox.addWidget(lb1)
        hbox.addWidget(lb2)
        hbox.addWidget(btn)
        hbox.addWidget(btn2)
        
        
        self.setLayout(hbox)
        self.move(300, 300)
        self.setWindowTitle('E-See')
        #self.show()
    
    def paizhao(self):
        self.frameThread.paizhao = 1
        self.frameThread2.paizhao = 1
    
    
    def showDate(self, date):
        self.lb1.setText(date.toString())
    
    def get_frame(self):
        _, frame = self.capture.read()
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)

    def switch(self):
        self.switch_window.emit()



class FrameThread2(QThread):
    imgLab = None
    device = None
    paizhao = 0
    """攝像頭拍照執行緒，攝像頭拍照耗時較長容易卡住UI"""
    
    def __init__(self, deviceIndex, imgLab):
        QThread.__init__(self)
        self.imgLab = imgLab
        self.deviceIndex = deviceIndex
        self.device = cv2.VideoCapture(self.deviceIndex)  # 從攝像頭中取得視訊
        self.device.set(cv2.CAP_PROP_FRAME_WIDTH, 1600)
        self.device.set(cv2.CAP_PROP_FRAME_HEIGHT, 1200)
    
    def run(self):
        if self.device.isOpened():
            try:
                while True:
                    ret, frame = self.device.read()
                    height, width, bytesPerComponent = frame.shape
                    bytesPerLine = bytesPerComponent * width
                    # 變換彩色空間順序
                    cv2.cvtColor(frame, cv2.COLOR_BGR2RGB, frame)
                    # 轉為QImage物件
                    image = QImage(frame.data, width, height, bytesPerLine, QImage.Format_RGB888)
                    if self.paizhao == 1:
                        image.save('./origin/takephoto.png')
                        self.paizhao = 0
                        pixmap = QPixmap.fromImage(image)
                        pixmap = pixmap.scaled(400, 300, QtCore.Qt.KeepAspectRatio)
                        self.imgLab.setPixmap(pixmap)
                        objectdetection()
                        outcome('./result/audio/objoutcome.txt')
            finally:
                self.device.release()

    def destroyed(self, QObject=None):
        self.device.release()
    
    def switch(self):
        self.switch_window.emit()

### window 3.2
class MainWindow2(QWidget):
    
    switch_window = QtCore.pyqtSignal()
    
    def __init__(self, camera_index=0, fps=30):
        super().__init__()
        
        self.capture = cv2.VideoCapture(camera_index)
        self.dimensions = self.capture.read()[1].shape[1::-1]
        
        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)
        
        view = QGraphicsView(self)
        view.setScene(scene)
        
        text = QLabel('準備就緒', self)
        text.move(50, 575)
        
        layout = QVBoxLayout(self)
        layout.addWidget(view)
        #layout.addWidget(text)
        
        timer = QTimer(self)
        timer.setInterval(int(1000/fps))
        timer.timeout.connect(self.get_frame)
        timer.start()
        
        self.initUI()
    
    def initUI(self):
        hbox = QHBoxLayout(self)
        
        lb1 = QLabel(self)
        lb2 = QLabel(self)
        
        btn = QPushButton(self)
        btn.setText("拍照")
        btn.move(800, 530)
        btn.clicked.connect(self.paizhao)
        
        btn2 = QPushButton(self)
        btn2.setText("Next")
        btn2.move(800, 500)
        btn2.clicked.connect(self.switch)
        
        self.frameThread = FrameThread2(0,lb1)
        self.frameThread.start()
        self.frameThread2 = FrameThread2(1,lb2)
        self.frameThread2.start()
        
        hbox.addWidget(lb1)
        hbox.addWidget(lb2)
        hbox.addWidget(btn)
        hbox.addWidget(btn2)
        
        
        self.setLayout(hbox)
        self.move(300, 300)
        self.setWindowTitle('E-See')
    #self.show()
    
    def paizhao(self):
        self.frameThread.paizhao = 1
        self.frameThread2.paizhao = 1
    
    
    def showDate(self, date):
        self.lb1.setText(date.toString())
    
    def get_frame(self):
        _, frame = self.capture.read()
        image = QImage(frame, *self.dimensions, QImage.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(image)
        self.pixmapItem.setPixmap(pixmap)
    
    def switch(self):
        self.switch_window.emit()


### window 4
class OutComeUi(QWidget):

    switch_window = QtCore.pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.initUI()
        self.wavplay()
    
    def initUI(self):
        self.setWindowTitle("OutComeUI")
        
        layout = QtWidgets.QGridLayout()
        
        self.label = QtWidgets.QLabel()
        layout.addWidget(self.label)
        
        self.button = QtWidgets.QPushButton('Return')
        self.button.clicked.connect(self.close)
        
        layout.addWidget(self.button)
        
        self.setLayout(layout)
        
        self.resize(250, 150)
        self.move(300, 300)
        pic = QPixmap('./origin/volume.png')
        self.lb = QLabel(self)
        self.lb.setGeometry(50, 50, 150, 30)
        self.lb.setPixmap(pic)
    
    
    def switch(self):
        self.switch_window.emit()
    
    def wavplay(self):
        self.sound = QSound('./result/audio/outcome.wav')
        self.sound.play()



class Controller:
    def __init__(self):
        pass
    
    def show_audio(self):
        self.audio = AudioUi()
        self.audio.switch_window.connect(self.show_command)
        self.audio.show()
    
    def show_command(self):
        self.window = CommandUi()
        #self.c = self.window.command()
        self.window.switch_window.connect(self.show_camera)
        self.audio.close()
        self.window.show()

    
    def show_camera(self):
        self.camera = MainWindow()
        self.cameraobj = MainWindow2()
        
        #self.window.close()
        #self.camera.show()
        with open('./result/audio/command.txt', 'r') as f:
            self.c = f.read().strip()
            #print(self.c)
        
        if self.c == "閱讀" or self.c == "閱讀模式":
            self.window.close()
            self.camera.show()
        elif self.c == "用餐" or self.c == "用餐模式":
            self.window.close()
            self.cameraobj.show()
        elif self.c == "沒事" or self.c == "結束":
            self.window.close()
            self.camera.close()
        else:
            self.window.close()
            self.camera.close()
        
        self.camera.switch_window.connect(self.show_outcome)
        self.cameraobj.switch_window.connect(self.show_outcome)

    def show_outcome(self):
        self.output = OutComeUi()
        self.camera.close()
        self.cameraobj.close()
        self.output.show()




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Controller()
    ex.show_audio()
    sys.exit(app.exec_())
