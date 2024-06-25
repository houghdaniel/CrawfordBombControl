# GUI
import sys
import os
import time
import threading

#from bombControl import BombControl
from labjack import ljm

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6 import QtGui
from PySide6.QtUiTools import QUiLoader

class BombControl:

    def __init__(self):
        self.handle = ljm.openS("T4", "ANY", "ANY")
        self.fill_valve = "TDAC7"
        self.exhaust_valve = "DAC1"
        self.ignite = ""
        self.transducer = "AIN3"

        self.open = 0
        self.close = 5
        self.set_pressure = 0
        self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600

        window.measuredPressureField.setText(self.measured_pressure)

    def fill(self):
        ljm.eWriteName(self.handle, self.fill_valve, self.open) # Open fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.close) # Close exhaust valve

        self.set_pressure = window.setPressureField.text() # Get set pressure
        
        # While measured pressure is below set pressure, keep checking measured pressure and updating field
        while self.set_pressure > self.measured_pressure:
            self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600
            window.measuredPressureField.setText(self.measured_pressure)
        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve




    def vent(self):
        # First, end data recording
        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.open) # Open exhaust valve
        

    def ignition(self):
        # Begin data recording and trigger pulse for ignition
        pass
        


loader = QUiLoader()
bomb = BombControl()

def mainwindow_setup(w):
    w.setWindowTitle("Crawford Bomb Control")
    w.fillButton.clicked.connect(fill_button_pressed) 
    w.ventButton.clicked.connect(vent_button_pressed) 
    w.ignitionButton.clicked.connect(ignition_button_pressed)

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





