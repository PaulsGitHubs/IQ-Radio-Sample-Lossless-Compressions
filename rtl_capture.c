#include <stdio.h>
#include <stdlib.h>
#include <rtl-sdr.h>
#include <pthread.h>
#include <unistd.h>
#include <signal.h>

#define BUF_LEN (8192)

rtlsdr_dev_t *dev = NULL;
FILE *file = NULL;

void rtl_callback(unsigned char *buf, uint32_t len, void *ctx) {
    FILE *file = (FILE *)ctx;
    fwrite(buf, 1, len, file);
}

void* listen_for_input(void* arg) {
    char c;
    while (1) {
        c = getchar();
        if (c == ' ' || c == '\n' || c == 'c') {
            break;
        }
    }
    exit(0); // Terminates the program if any of the exit keys are pressed.
}

void cleanup(int sig_num) {
    printf("\nClosing...\n");

    // Stop the asynchronous reader.
    if (dev != NULL) {
        rtlsdr_cancel_async(dev);
    }

    // Close the RTL-SDR device.
    if (dev != NULL) {
        rtlsdr_close(dev);
    }

    // Close the output file.
    if (file != NULL) {
        fclose(file);
    }
    exit(0);
}

int main() {
    struct sigaction sa;
    sa.sa_handler = cleanup;
    sigaction(SIGINT, &sa, NULL);

    pthread_t input_thread;
    pthread_create(&input_thread, NULL, listen_for_input, NULL);

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
    file = fopen("input.bin", "wb");
    if (file == NULL) {
        fprintf(stderr, "Failed to open output file.\n");
        return 1;
    }

    printf("To stop the program, press 'Spacebar', 'Enter', 'c' or 'Ctrl+C'\n");

    // Start the RTL-SDR's asynchronous reader.
    if (rtlsdr_read_async(dev, rtl_callback, file, 0, BUF_LEN) < 0) {
        fprintf(stderr, "Failed to start async reading.\n");
        return 1;
    }

    pthread_join(input_thread, NULL); // Wait for the input thread to finish
    return 0;
}
