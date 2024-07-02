import csv
import time
from labjack import ljm

import settings as s

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
        self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600 - s.pressure_offset

        window.measuredPressureField.setText("%.2f"%(self.measured_pressure))

    def fill(self):
        ljm.eWriteName(self.handle, self.fill_valve, self.open) # Open fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.close) # Close exhaust valve

        self.set_pressure = float(self.window.setPressureField.text()) # Get set pressure
        
        # While measured pressure is below set pressure, keep checking measured pressure and updating field
        while self.set_pressure > self.measured_pressure:
            self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * 600 - s.pressure_offset
            self.window.measuredPressureField.setText("%.2f"%(self.measured_pressure))
        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve

    def vent(self):
        # First, end data recording
        s.running = False
        save_file = self.window.dataSaveFolderField.text() + self.window.sampleIDField.text() + ".csv"

        with open(save_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["time","voltage","pressure"])
            for i in range(len(s.times)):
                writer.writerow([s.times[i],s.voltages[i],s.pressures[i]])
        print("Data written to " + save_file)

        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.open) # Open exhaust valve

    def ignition(self):
        # Begin data recording and trigger pulse for ignition
        s.running = True

        start_time = time.time()

        while s.running:
            t = time.time() - start_time
            v = ljm.eReadName(self.handle, self.transducer)
            p = v * 600 - s.pressure_offset

            s.times.append(t)
            s.voltages.append(v)
            s.pressures.append(p)

            time.sleep(1/100)

    def update(self):
        p = ljm.eReadName(self.handle, self.transducer) * 600 - s.pressure_offset
        self.window.measuredPressureField.setText("%.2f"%(p))
