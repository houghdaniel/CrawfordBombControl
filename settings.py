v_mult = 600
pressure_offset = 8

hz = 100

# DAC IO ports
fill_valve = "TDAC7"
exhaust_valve = "DAC1"
ignite = "DAC0"
transducer = "AIN3"

# Lists for data
times = []
voltages = []
pressures = []
running = False

# List of forbidden characters for filename
forbidden = ['*', '?', '<', '>', ':', '"', "'", '\\', '/', '|']