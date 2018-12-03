#! /usr/bin/python3
# coding = utf-8

import cv2
import sys
from run import *
from audioui import *
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QGraphicsScene, QGraphicsView, QPushButton


class Run(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('E-See')
        self.show()



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    w = AudioUi()

    sys.exit(app.exec_())

