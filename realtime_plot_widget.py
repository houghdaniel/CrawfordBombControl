from PySide6.QtWidgets import QWidget, QVBoxLayout
from PySide6.QtCore import QTimer

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from collections import deque

import settings as s

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
        self.plot_line.set_data(s.times, s.pressures)

        if s.times:
            last_time = s.times[-1]
            self.axes.set_xlim(max(0,last_time - 10), last_time)
            self.axes.set_ylim(0, max(s.pressures))

        self.canvas.draw()