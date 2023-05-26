# IQ-Sample-Compression-with-FFT-and-DWT

This project involves signal processing and compression of IQ samples from a Software Defined Radio (SDR). Various signal processing techniques such as FFT, DWT, DCT, and DST are applied to the data, and the results are subsequently compressed using various algorithms.

## Signal Processing

- Fast Fourier Transform (FFT)
- Discrete Wavelet Transform (DWT)
- Discrete Cosine Transform (DCT)
- Discrete Sine Transform (DST)

## Compression Algorithms

The following compression methods are tested in this project:

- gzip
- bz2
- lzma (xz)
- zlib
- zip
- tar
- lz4
- brotli

## Results

The compression results in terms of output file sizes for some of the top performing algorithms:

- output_dct.bin.brotli: 53.18 MB
- output_dst.bin.brotli: 53.18 MB
- output_dct.bin.xz: 53.31 MB
- output_dst.bin.xz: 53.31 MB
- output_dct.bin.gz: 53.86 MB
- output_dct.bin.zip: 53.86 MB
- output_dct.bin.tar.gz: 53.87 MB
- output_dst.bin.zlib: 53.87 MB
- output_dst.bin.gz: 53.87 MB
- output_dst.bin.zip: 53.87 MB
- output_dst.bin.tar.gz: 53.87 MB

The files were sorted from smallest to largest. The brotli, xz (lzma), and gzip compression methods provided the best results in terms of space reduction.

## Running the Project

Please make sure to install all required Python packages before running the scripts. Python 3 is recommended.

## Future Work

Further compression methods and signal processing techniques will be explored to find the most efficient process for handling IQ samples from SDRs.

## Contributing

Please feel free to fork the project, make improvements, and open a pull request.

## Overview

The `rtl_capture.c` file captures the IQ signals:

1. Opens RTL SDR 
2. Starts capture
3. Then saves the file in binary

The `compress.cpp` file performs the following steps:

1. Reads the SDR IQ samples from a binary file.
2. Applies FFT to the samples.
3. Performs a wavelet transform on the FFT output.
4. Stores the transformed data in binary files for the real and imaginary parts separately.

The `decompress.cpp` file performs the inverse operations:

1. Reads the wavelet-transformed data from binary files.
2. Applies inverse wavelet transform to the data.
3. At this stage, the output is the FFT transformed data. 

Please note that to retrieve the original time-domain signal, you would need to apply inverse FFT to the output.

## Dependencies

This project requires the FFTW and WaveLib libraries. Please ensure these libraries are properly installed and linked when building the project.

- Installing wavelib
```bash
#clone it
git clone https://github.com/rafat/wavelib
# Navigate to the 'src' directory in your local copy of the 'wavelib' repository
cd wavelib
# Compile all .c files in the directory to .o files
gcc -c *.c

# Combine all .o files into a single static library file
ar rcs libwavelib.a *.o

# Move the static library file to a directory where the linker can find it
sudo mv libwavelib.a /usr/local/lib/

# Copy all header files to a directory where the compiler can find them
sudo cp ../inc/*.h /usr/local/include/
```

## Building

1. Compile `rtl_capture.c` using a C compiler (gcc -o rtl_capture rtl_capture.c -lrtlsdr -lpthread) and start scan so you have something to try it on...
2. Compile `compress.c` using a C++ compiler (g++ -o compress compress.cpp -lfftw3 -lwavelib), linking the FFTW and WaveLib libraries.
3. Run the program with the binary file of IQ samples as input.
4. Compile `decompress.cpp` using a C++ (g++ -o decompress decompress.cpp -lwavelib) compiler, linking the WaveLib library.
5. Run the program to perform inverse wavelet transform on the transformed data.

Compile compress_image.cpp with g++ -std=c++17 compress_image.cpp -o compress_image -I/usr/include/opencv4 -L/usr/local/lib -lopencv_core -lopencv_imgcodecs -lopencv_imgproc -lstdc++fs


## Notes

Remember to set the number of samples (N) as per your input data. In these scripts, we assume N = 1024. Also, adjust the wavelet type and levels of wavelet decomposition according to your requirements. The default wavelet used in this project is Daubechies 4 (db4) with 4 levels of decomposition.
