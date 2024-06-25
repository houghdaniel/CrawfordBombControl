# GUI
import sys
import os
from bombControl import BombControl
import threading
from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6 import QtGui
from PySide6.QtUiTools import QUiLoader


#class MainWindow(QMainWindow):
#    def __init__(self):
#        super().__init__()
#        self.bomb = BombControl()
#        self.setWindowTitle("Crawford Bomb Control")
#
#        button = QPushButton("Start")
#        button.setFixedSize(QSize(100,50))
#        button.clicked.connect(self.button_pressed)
#
#        self.setMinimumSize(QSize(800,600))
#
#        self.setCentralWidget(button)
#        
#    
#    def button_pressed(self):
#        print("Clicked")
#        t1 = threading.Thread(target=self.bomb.fill())
#        t1.start()

loader = QUiLoader()
bomb = BombControl()

def mainwindow_setup(w):
    w.setWindowTitle("Crawford Bomb Control")
    w.fillButton.clicked.connect(fill_button_pressed) #stop DAC1
    w.ventButton.clicked.connect(vent_button_pressed) #release DAC0
    w.ignitionButton.clicked.connect(ignition_button_pressed) #run TDAC7

def fill_button_pressed():
    print("fill pressed\n")
    tf = threading.Thread(target=bomb.fill())
    tf.start()

def vent_button_pressed():
    print("vent pressed\n")
    tv = threading.Thread(target=bomb.vent())
    tv.start()

def ignition_button_pressed():
    print("ignition pressed\n")
    ti = threading.Thread(target=bomb.ignition())
    ti.start()


app = QApplication([])

window = loader.load("mainwindow.ui", None)
mainwindow_setup(window)
window.show()
app.exec()

