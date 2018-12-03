#! /usr/bin/python3
# coding = utf-8

import cv2
import sys
from audio import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsScene, QGraphicsView, QPushButton


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
    
    def __init__(self,deviceIndex,imgLab):
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
            finally:
                self.device.release()

    def destroyed(self, QObject=None):
        self.device.release()

class MainWindow(QWidget):
    def __init__(self, camera_index=0, fps=30):
        super().__init__()
        
        self.capture = cv2.VideoCapture(camera_index)
        self.dimensions = self.capture.read()[1].shape[1::-1]
        
        scene = QGraphicsScene(self)
        pixmap = QPixmap(*self.dimensions)
        self.pixmapItem = scene.addPixmap(pixmap)
        
        view = QGraphicsView(self)
        view.setScene(scene)
        
        text = QLabel('E-See', self)
        
        layout = QVBoxLayout(self)
        layout.addWidget(view)
        layout.addWidget(text)
        
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
        btn.move(800, 520)
        btn.clicked.connect(self.paizhao)
        
        self.frameThread = FrameThread(0,lb1)
        self.frameThread.start()
        self.frameThread2 = FrameThread(1,lb2)
        self.frameThread2.start()
        
        hbox.addWidget(lb1)
        hbox.addWidget(lb2)
        hbox.addWidget(btn)
        
        self.setLayout(hbox)
        self.move(300, 300)
        self.setWindowTitle('E-See')
        self.show()
    
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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
