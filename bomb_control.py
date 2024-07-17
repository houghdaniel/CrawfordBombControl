import csv
import time
from labjack import ljm

import settings as s

class BombControl:

    def __init__(self, window):
        self.handle = ljm.openS("T4", "ANY", "ANY")
        self.fill_valve = s.fill_valve
        self.exhaust_valve = s.exhaust_valve
        self.ignite = s.ignite
        self.transducer = s.transducer
        self.window = window

        self.open = 0
        self.close = 5
        self.set_pressure = 0
        self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * s.v_mult - s.pressure_offset

        window.measuredPressureField.setText("%.2f"%(self.measured_pressure))

        # Close fill, exhaust, and make sure ignition relay is open
        ljm.eWriteName(self.handle, self.fill_valve, self.close)
        ljm.eWriteName(self.handle, self.exhaust_valve, self.close)
        ljm.eWriteName(self.handle, self.ignite, self.open)

    def fill(self):
        ljm.eWriteName(self.handle, self.exhaust_valve, self.close) # Close exhaust valve
        ljm.eWriteName(self.handle, self.fill_valve, self.open) # Open fill valve
        

        self.set_pressure = float(self.window.setPressureField.text()) # Get set pressure
        
        # While measured pressure is below set pressure, keep checking measured pressure and updating field
        while self.set_pressure > self.measured_pressure:
            self.measured_pressure = ljm.eReadName(self.handle, self.transducer) * s.v_mult - s.pressure_offset
            self.window.measuredPressureField.setText("%.2f"%(self.measured_pressure))
        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve

    def vent(self):
        # First, end data recording and log to file
        s.running = False
        sample_ID = self.window.sampleIDField.text()

        # Replace special characters in sample ID filename with '_'
        for symbol in s.forbidden:
            if symbol in sample_ID:
                sample_ID = sample_ID.replace(symbol, '_')

        save_file = self.window.dataSaveFolderField.text() + sample_ID + ".csv"

        with open(save_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["time","voltage","pressure"])
            for i in range(len(s.times)):
                writer.writerow([s.times[i],s.voltages[i],s.pressures[i]])
        print("Data written to " + save_file)
        ljm.eWriteName(self.handle, self.ignite, self.open) # Open relay to ignition circuit

        # After data is saved, clear arrays to be able to start new experiment without restarting program
        s.times.clear()
        s.voltages.clear()
        s.pressures.clear()

        ljm.eWriteName(self.handle, self.fill_valve, self.close) # Close fill valve
        ljm.eWriteName(self.handle, self.exhaust_valve, self.open) # Open exhaust valve

    def ignition(self):
        # Begin data recording
        s.running = True
        # Close relay for ignition
        ljm.eWriteName(self.handle, self.ignite, self.close)

        # TODO: add another pulse for triggering other equipment

        start_time = time.time()

        while s.running:
            t = time.time() - start_time
            v = ljm.eReadName(self.handle, self.transducer)
            p = v * s.v_mult - s.pressure_offset

            s.times.append(t)
            s.voltages.append(v)
            s.pressures.append(p)

            time.sleep(1/s.hz)

    def purge(self):
        ljm.eWriteName(self.handle, self.exhaust_valve, self.open)
        ljm.eWriteName(self.handle, self.fill_valve, self.open)
        time.sleep(10)
        ljm.eWriteName(self.handle, self.fill_valve, self.close)


    def update(self):
        p = ljm.eReadName(self.handle, self.transducer) * s.v_mult - s.pressure_offset
        self.window.measuredPressureField.setText("%.2f"%(p))
