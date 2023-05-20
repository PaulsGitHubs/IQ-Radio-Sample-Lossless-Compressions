#include <stdio.h>
#include <stdlib.h>
#include <rtl-sdr.h>

#define BUF_LEN (8192)

void rtl_callback(unsigned char *buf, uint32_t len, void *ctx) {
    FILE *file = (FILE *)ctx;

    // Write the data to the file.
    fwrite(buf, 1, len, file);
}

int main() {
    rtlsdr_dev_t *dev = NULL;
    int dev_index = 0; // Use the first RTL-SDR device by default.

    // Open the RTL-SDR device.
    if (rtlsdr_open(&dev, dev_index) < 0) {
        fprintf(stderr, "Failed to open RTL-SDR device #%d.\n", dev_index);
        return 1;
    }

    // Set the sample rate.
    uint32_t sample_rate = 2048000; // 2.048 MHz
    if (rtlsdr_set_sample_rate(dev, sample_rate) < 0) {
        fprintf(stderr, "Failed to set sample rate.\n");
        return 1;
    }

    // Set the center frequency.
    uint32_t frequency = 100000000; // 100 MHz
    if (rtlsdr_set_center_freq(dev, frequency) < 0) {
        fprintf(stderr, "Failed to set center frequency.\n");
        return 1;
    }

    // Open the output file.
    FILE *file = fopen("input.bin", "wb");
    if (file == NULL) {
        fprintf(stderr, "Failed to open output file.\n");
        return 1;
    }

    // Start the RTL-SDR's asynchronous reader.
    if (rtlsdr_read_async(dev, rtl_callback, file, 0, BUF_LEN) < 0) {
        fprintf(stderr, "Failed to start async reading.\n");
        return 1;
    }

    // Close the RTL-SDR device.
    rtlsdr_close(dev);

    // Close the output file.
    fclose(file);

    return 0;
}
