import numpy as np
from rtlsdr import RtlSdr
import signal
import sys

# create a new instance of the SDR
sdr = RtlSdr()

# configure device
sdr.sample_rate = 2.048e6  # 2.048 MHz
sdr.center_freq = 100e6     # 100 MHz
sdr.freq_correction = 60   # PPM
sdr.gain = 'auto'

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    # cleanup
    sdr.close()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C to stop the recording')

# start the capturing
while True:
    # read_samples returns a numpy array of complex numbers and blocks until data is available
    samples = sdr.read_samples(256*1024) # 256K samples 
    for i in range(0, len(samples), 1024):
        buffer = samples[i:i+1024]
        # save the data to the file
        with open('input.bin', 'ab') as f:
            buffer.tofile(f)

# to stop capturing, press Ctrl+C
