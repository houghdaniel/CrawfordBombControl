# GUI
import sys
import threading

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader

from bomb_control import BombControl
from realtime_plot_widget import RealTimePlotWidget

import settings as s

def mainwindow_setup(w):
    w.setWindowTitle("Crawford Bomb Control")
    w.fillButton.clicked.connect(fill_button_pressed) 
    w.ventButton.clicked.connect(vent_button_pressed) 
    w.ignitionButton.clicked.connect(ignition_button_pressed)
    w.purgeButton.clicked.connect(purge_button_pressed)

def plotwindow_setup(w):
    w.setWindowTitle("Real-Time Pressure vs. Time Plot")
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

def purge_button_pressed():
    print("purge pressed\n")
    tp = threading.Thread(target=bomb.purge)
    tp.daemon = True
    tp.start()

loader = QUiLoader()
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