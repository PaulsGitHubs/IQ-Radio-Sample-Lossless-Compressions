# IQ-Sample-Compression-with-FFT-and-DWT
hahaha, lets see if this works...
## I got inspired by a Spacex video where they use FFT and DWT to transform data for their rocket engine simulation... Let's try it for Radio Wave IQ samples

    Wavelet Type: For RTL-SDR IQ data, it would be better to start with Daubechies wavelets (dbN). Daubechies wavelets, especially of higher orders, are a popular choice for signal processing applications because they can represent a wide variety of signals well. You could start with db4 or db6, and adjust as necessary based on your results.

    Extension Mode: The extension mode for the DWT doesn't typically have a large effect on the result, especially for long signals. You can start with the symmetric extension ("sym") because it makes no assumptions about the signal beyond the boundary and thus can be a safe choice.

    Decomposition Levels: The number of decomposition levels you should use depends on the specific features you're interested in your data. A larger number of levels will give you more detailed frequency information, but at the cost of losing some time information. Conversely, fewer levels will preserve more time information, but at a coarser frequency resolution. A good starting point might be around 3-4 levels, but this would largely depend on your application and the characteristics of your data.

## Overview

The `rtl_capture.c` file captures the IQ signals:

1. Opens RTL SDR 
2. Starts capture
3. Then saves the file in binary

The `compress.c` file performs the following steps:

1. Reads the SDR IQ samples from a binary file.
2. Applies FFT to the samples.
3. Performs a wavelet transform on the FFT output.
4. Stores the transformed data in binary files for the real and imaginary parts separately.

The `decompress.c` file performs the inverse operations:

1. Reads the wavelet-transformed data from binary files.
2. Applies inverse wavelet transform to the data.
3. At this stage, the output is the FFT transformed data. 

Please note that to retrieve the original time-domain signal, you would need to apply inverse FFT to the output.

## Dependencies

This project requires the FFTW and WaveLib libraries. Please ensure these libraries are properly installed and linked when building the project.

## Building

1. Compile `main.cpp` using a C++ compiler, linking the FFTW and WaveLib libraries.
2. Run the program with the binary file of IQ samples as input.
3. Compile `decompress.cpp` using a C++ compiler, linking the WaveLib library.
4. Run the program to perform inverse wavelet transform on the transformed data.

## Notes

Remember to set the number of samples (N) as per your input data. In these scripts, we assume N = 1024. Also, adjust the wavelet type and levels of wavelet decomposition according to your requirements. The default wavelet used in this project is Daubechies 4 (db4) with 4 levels of decomposition.
