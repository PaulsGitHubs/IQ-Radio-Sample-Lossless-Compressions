import numpy as np
import pywt
from scipy.fftpack import dct
from scipy.fftpack import dst
def perform_fft(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = np.fromfile(f, dtype=np.float32)

    # Perform FFT
    fft_data = np.fft.fft(data)

    # Write FFT transformed data
    with open(output_file, 'wb') as f:
        fft_data.astype(np.complex64).tofile(f)

def perform_dwt(input_file, output_file_cA, output_file_cD):
    with open(input_file, 'rb') as f:
        data = np.fromfile(f, dtype=np.float32)

    # Perform DWT
    dwt_data = pywt.dwt(data, 'db5')

    # Write DWT transformed data
    with open(output_file_cA, 'wb') as f:
        dwt_data[0].astype(np.float32).tofile(f)

    with open(output_file_cD, 'wb') as f:
        dwt_data[1].astype(np.float32).tofile(f)

def perform_dct(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = np.fromfile(f, dtype=np.float32)

    # Perform DCT
    dct_data = dct(data)

    # Write DCT transformed data
    with open(output_file, 'wb') as f:
        dct_data.astype(np.float32).tofile(f)
        
def perform_dst(input_file, output_file):
    with open(input_file, 'rb') as f:
        data = np.fromfile(f, dtype=np.float32)

    dst_data = dst(data)  # use dst here

    with open(output_file, 'wb') as f:
        dst_data.astype(np.float32).tofile(f)

        
perform_fft('input.bin', 'output_fft.bin')
perform_dwt('input.bin', 'output_dwt_cA.bin', 'output_dwt_cD.bin')
perform_dct('input.bin', 'output_dct.bin')
perform_dst('input.bin', 'output_dst.bin')
perform_dwt('output_fft.bin','fft_dwtcA.bin', 'fft_dwtcD.bin' )
perform_dct('output_fft.bin','fft_dct.bin')
perform_dst('output_fft.bin', 'fft_dst.bin')


