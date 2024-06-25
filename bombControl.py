from labjack import ljm
import time


# Functions for bomb control

# fill, vent, begin buttons
# save function

# open labjack function

class BombControl:

    def __init__(self):
        self.handle = ljm.openS("T4", "ANY", "ANY")
        self.fill_valve = ""
        self.exhaust_valve = ""
        self.ignite = ""

    def fill(self):
        # fill valve open exhaust valve closed, while loop until desired pressure met, updating measured pressure as we go
        ljm.eWriteName(self.handle, "DAC1", 5)
        time.sleep(0.25)
        ljm.eWriteName(self.handle, "DAC1", 0)

    def vent(self):
        # write
        ljm.eWriteName(self.handle, "DAC0", 5)
        time.sleep(0.25)
        ljm.eWriteName(self.handle, "DAC0", 0)

    def ignition(self):
        ljm.eWriteName(self.handle, "TDAC7", 5)
        time.sleep(0.25)
        ljm.eWriteName(self.handle, "TDAC7", 0)
        