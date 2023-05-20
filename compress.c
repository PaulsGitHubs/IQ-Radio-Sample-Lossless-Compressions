#include <fftw3.h>
#include <fstream>
#include <vector>
#include "wavelib.h"  // Include Wavelib library

const int N = 1024; // Assuming that you have 1024 samples

int main() {
    // Load the radio wave data from a file
    std::ifstream input("input.bin", std::ios::binary);

    // Perform FFT on the data.
    fftw_complex *in, *out;
    fftw_plan p;
    in = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
    out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * N);
    p = fftw_plan_dft_1d(N, in, out, FFTW_FORWARD, FFTW_ESTIMATE);

    // Read the data from binary file and fill in[] array
    if(input.is_open()) {
        for(int i = 0; i < N; i++) {
            double real_part;
            input.read((char*)&real_part, sizeof(double));
            in[i][0] = real_part; // Real part of the sample
            in[i][1] = 0; // Imaginary part of the sample is assumed to be 0
        }
    }
    input.close();

    fftw_execute(p); // Now out[] contains the FFT of your data.

    // Perform wavelet transform on the FFT data.
    // Wavelib requires the input data in a one-dimensional array.
    double* fft_out_real = new double[N];
    double* fft_out_imag = new double[N];
    for(int i = 0; i < N; i++) {
        fft_out_real[i] = out[i][0]; // Real part of FFT output
        fft_out_imag[i] = out[i][1]; // Imaginary part of FFT output
    }

    // Perform discrete wavelet transform on real part
    wave_object obj_real;
    wt_object wt_real;
    obj_real = wave_init("db4"); // Initialize wavelet
    wt_real = wt_init(obj_real, "dwt", N, 4); // Initialize discrete wavelet transform object with 4 levels
    setDWTExtension(wt_real, "sym");  // Set extension mode
    setWTConv(wt_real, "direct");  // Set convolution type
    dwt(wt_real, fft_out_real); // Perform DWT on FFT output

    // Save the DWT real output to a binary file
    std::ofstream output_real("dwt_real.bin", std::ios::binary);
    if(output_real.is_open()) {
        for(int i = 0; i < wt_real->outlength; i++) {
            output_real.write((char*)&wt_real->output[i], sizeof(double));
        }
    }
    output_real.close();

    // Perform discrete wavelet transform on imaginary part
    wave_object obj_imag;
    wt_object wt_imag;
    obj_imag = wave_init("db4"); // Initialize wavelet
    wt_imag = wt_init(obj_imag, "dwt", N, 4); // Initialize discrete wavelet transform object with 4 levels
    setDWTExtension(wt_imag, "sym");  // Set extension mode
    setWTConv(wt_imag, "direct");  // Set convolution type
    dwt(wt_imag, fft_out_imag); // Perform DWT on FFT output

    // Save the DWT imaginary output to a binary file
    std::ofstream output_imag("dwt_imag.bin", std::ios::binary);
    if(output_imag.is_open()) {
        for(int i = 0; i < wt_imag->outlength; i++) {
            output_imag.write((char*)&wt_imag->output[i], sizeof(double));
        }
    }
    output_imag.close();

    // Cleanup
    wave_free(obj_real);
    wt_free(wt_real);
    wave_free(obj_imag);
    wt_free(wt_imag);

    fftw_destroy_plan(p);
    fftw_free(in);
    fftw_free(out);
    delete[] fft_out_real;
    delete[] fft_out_imag;

    return 0;
}

