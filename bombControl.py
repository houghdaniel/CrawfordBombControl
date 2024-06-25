from labjack import ljm
import time


# Functions for bomb control

# fill, vent, begin buttons
# save function

# open labjack function

class BombControl:

    def __init__(self):
        self.handle = ljm.openS("T4", "ANY", "ANY")
        self.fill_valve = "TDAC7"
        self.exhaust_valve = "DAC1"
        self.ignite = ""
        self.open = 0
        self.close = 5

    def fill(self):
        # fill valve open exhaust valve closed, while loop until desired pressure met, updating measured pressure as we go
        ljm.eWriteName(self.handle, self.fill_valve, self.open)
        ljm.eWriteName(self.handle, self.exhaust_valve, self.close)


    def vent(self):
        # write
        ljm.eWriteName(self.handle, "DAC0", 5)
        time.sleep(0.25)
        ljm.eWriteName(self.handle, "DAC0", 0)

    def ignition(self):
        ljm.eWriteName(self.handle, "TDAC7", 5)
        time.sleep(0.25)
        ljm.eWriteName(self.handle, "TDAC7", 0)
        