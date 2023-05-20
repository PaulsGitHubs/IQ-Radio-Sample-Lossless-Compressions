#include <fstream>
#include "wavelib.h"  // Include Wavelib library

const int N = 1024; // Assuming that you have 1024 samples

int main() {
    // Read the real part from binary file
    double* dwt_real = new double[N];
    std::ifstream input_real("dwt_real.bin", std::ios::binary);
    if(input_real.is_open()) {
        input_real.read((char*)dwt_real, sizeof(double) * N);
    }
    input_real.close();

    // Read the imaginary part from binary file
    double* dwt_imag = new double[N];
    std::ifstream input_imag("dwt_imag.bin", std::ios::binary);
    if(input_imag.is_open()) {
        input_imag.read((char*)dwt_imag, sizeof(double) * N);
    }
    input_imag.close();

    // Perform inverse discrete wavelet transform on real part
    wave_object obj_real;
    wt_object wt_real;
    obj_real = wave_init("db4"); // Initialize wavelet
    wt_real = wt_init(obj_real, "idwt", N, 4); // Initialize inverse discrete wavelet transform object with 4 levels
    setDWTExtension(wt_real, "sym");  // Set extension mode
    setWTConv(wt_real, "direct");  // Set convolution type
    idwt(wt_real, dwt_real); // Perform IDWT on real part

    // Perform inverse discrete wavelet transform on imaginary part
    wave_object obj_imag;
    wt_object wt_imag;
    obj_imag = wave_init("db4"); // Initialize wavelet
    wt_imag = wt_init(obj_imag, "idwt", N, 4); // Initialize inverse discrete wavelet transform object with 4 levels
    setDWTExtension(wt_imag, "sym");  // Set extension mode
    setWTConv(wt_imag, "direct");  // Set convolution type
    idwt(wt_imag, dwt_imag); // Perform IDWT on imaginary part

    // Now, the variable wt_real->output and wt_imag->output contain the inverse DWT data which are the FFT outputs.

    // Cleanup
    wave_free(obj_real);
    wt_free(wt_real);
    wave_free(obj_imag);
    wt_free(wt_imag);

    delete[] dwt_real;
    delete[] dwt_imag;

    return 0;
}
