# IQ-Sample-Compression-with-FFT-and-DWT
hahaha, lets see if this works...
## I got inspired by a Spacex video where they use FFT and DWT to transform data for their rocket engine simulation... Let's try it for Radio Wave IQ samples

    Wavelet Type: For RTL-SDR IQ data, it would be better to start with Daubechies wavelets (dbN). Daubechies wavelets, especially of higher orders, are a popular choice for signal processing applications because they can represent a wide variety of signals well. You could start with db4 or db6, and adjust as necessary based on your results.

    Extension Mode: The extension mode for the DWT doesn't typically have a large effect on the result, especially for long signals. You can start with the symmetric extension ("sym") because it makes no assumptions about the signal beyond the boundary and thus can be a safe choice.

    Decomposition Levels: The number of decomposition levels you should use depends on the specific features you're interested in your data. A larger number of levels will give you more detailed frequency information, but at the cost of losing some time information. Conversely, fewer levels will preserve more time information, but at a coarser frequency resolution. A good starting point might be around 3-4 levels, but this would largely depend on your application and the characteristics of your data.
