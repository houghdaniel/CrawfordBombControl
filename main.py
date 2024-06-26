# GUI
import sys
import time
import threading
import csv

from labjack import ljm

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout
from PySide6.QtUiTools import QUiLoader

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from collections import deque

times = []
voltages = []
pressures = []
running = False

pressure_offset = 8

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
        self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600 - pressure_offset

        window.measuredPressureField.setText("%.2f"%(self.measured_pressure))

    def fill(self):
        ljm.eWriteName(self.handle, self.fill_valve, self.open) # Open fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.close) # Close exhaust valve

        self.set_pressure = float(self.window.setPressureField.text()) # Get set pressure
        
        # While measured pressure is below set pressure, keep checking measured pressure and updating field
        while self.set_pressure > self.measured_pressure:
            self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600 - pressure_offset
            self.window.measuredPressureField.setText("%.2f"%(self.measured_pressure))
        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve

    def vent(self):
        # First, end data recording
        #global running
        #running = False

        save_file = self.window.dataSaveFolderField.text() + self.window.sampleIDField.text() + ".csv"
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
            p = v * 600 - pressure_offset

            times.append(t)
            voltages.append(v)
            pressures.append(p)

            time.sleep(1/100)

    def update(self):
        p = ljm.eReadName(self.handle, self.transducer) * 600 - pressure_offset
        self.window.measuredPressureField.setText("%.2f"%(p))

class RealTimePlotWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.figure, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        self.time = deque(maxlen=1000)
        self.pressure = deque(maxlen=1000)

        self.plot_line, = self.axes.plot([], [], 'b-')
        self.axes.set_xlabel("Time (s)")
        self.axes.set_ylabel("Pressure (psi)")
        self.axes.set_title("Pressure vs. Time")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(100)

    def update_plot(self):
        self.plot_line.set_data(times, pressures)

        if times:
            last_time = times[-1]
            self.axes.set_xlim(max(0,last_time - 10), last_time)
            self.axes.set_ylim(0, max(pressures))

        self.canvas.draw()

loader = QUiLoader()

def mainwindow_setup(w):
    w.setWindowTitle("Crawford Bomb Control")
    w.fillButton.clicked.connect(fill_button_pressed) 
    w.ventButton.clicked.connect(vent_button_pressed) 
    w.ignitionButton.clicked.connect(ignition_button_pressed)

def plotwindow_setup(w):
    w.setWindowTitle("Real-Time Presure vs. Time Plot")
    plot_widget = RealTimePlotWidget()
    w.setCentralWidget(plot_widget)

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

main_window = loader.load("mainwindow.ui", None)
mainwindow_setup(main_window)
main_window.show()

plot_window = QMainWindow()
plotwindow_setup(plot_window)
plot_window.show()

bomb = BombControl(main_window)

timer = QTimer()
timer.timeout.connect(bomb.update)
timer.start(100)

sys.exit(app.exec())