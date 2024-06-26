# GUI
import sys
import os
import time
import threading
import csv

from labjack import ljm

from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton
from PySide6 import QtGui
from PySide6.QtUiTools import QUiLoader

times = []
voltages = []
pressures = []
running = False

class BombControl:

    def __init__(self, window):
        self.handle = ljm.openS("T4", "ANY", "ANY")
        self.fill_valve = "TDAC7"
        self.exhaust_valve = "DAC1"
        self.ignite = ""
        self.transducer = "AIN3"
        self.window = window

        self.open = 0
        self.close = 5
        self.set_pressure = 0
        self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600

        window.measuredPressureField.setText("%.2f"%(self.measured_pressure))

    def fill(self):
        ljm.eWriteName(self.handle, self.fill_valve, self.open) # Open fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.close) # Close exhaust valve

        self.set_pressure = float(window.setPressureField.text()) # Get set pressure
        
        # While measured pressure is below set pressure, keep checking measured pressure and updating field
        while self.set_pressure > self.measured_pressure:
            self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600
            window.measuredPressureField.setText("%.2f"%(self.measured_pressure))
        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve

    def vent(self):
        # First, end data recording
        #global running
        #running = False

        save_file = window.dataSaveFolderField.text() + window.sampleIDField.text() + ".csv"
        global times, voltages, pressures

        with open(save_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["time","voltage","pressure"])
            for i in range(len(times)):
                writer.writerow([times[i],voltages[i],pressures[i]])
        print("Data written to " + save_file)

        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.open) # Open exhaust valve

    def ignition(self):
        # Begin data recording and trigger pulse for ignition
        global times, voltages, pressures

        #running = True

        start_time = time.time()

        while True:
            t = time.time() - start_time
            v = ljm.eReadName(self.handle, self.transducer)
            p = v * 600

            times.append(t)
            voltages.append(v)
            pressures.append(p)

            time.sleep(1/100)

    def update(self):
        p = ljm.eReadName(self.handle, self.transducer) * 600
        self.window.measuredPressureField.setText("%.2f"%(p))




loader = QUiLoader()

def mainwindow_setup(w):
    w.setWindowTitle("Crawford Bomb Control")
    w.fillButton.clicked.connect(fill_button_pressed) 
    w.ventButton.clicked.connect(vent_button_pressed) 
    w.ignitionButton.clicked.connect(ignition_button_pressed)

def fill_button_pressed():
    print("fill pressed\n")
    tf = threading.Thread(target=bomb.fill)
    tf.start()

def vent_button_pressed():
    print("vent pressed\n")
    bomb.vent()

def ignition_button_pressed():
    print("ignition pressed\n")
    ti = threading.Thread(target=bomb.ignition)
    ti.daemon = True
    ti.start()



app = QApplication([])

window = loader.load("mainwindow.ui", None)
mainwindow_setup(window)
window.show()
bomb = BombControl(window)

timer = QTimer()
timer.timeout.connect(bomb.update)
timer.start(100)




sys.exit(app.exec())
