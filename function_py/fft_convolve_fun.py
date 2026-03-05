import numpy as np
from scipy.fft import fft, ifft

# Utility function: pad array B to match the length of array A, centering the data
def fft_convolve(x, y):
    """
    Optimized FFT-based convolution implementation (supports complex numbers).
    
    Computes the linear convolution of two sequences x and y using the
    Fast Fourier Transform (FFT). This method is efficient for long signals,
    leveraging the convolution theorem: convolution in time domain equals
    pointwise multiplication in frequency domain.
    
    Parameters
    ----------
    x : array_like
        First input sequence.
    y : array_like
        Second input sequence.
        
    Returns
    -------
    result : ndarray
        The linear convolution of x and y, with length len(x) + len(y) - 1.
        The result preserves complex dtype if either input is complex.
    """
    n = len(x)
    m = len(y)
    out_len = n + m - 1
    
    # Determine FFT size as the smallest power of 2 >= out_len
    # (This improves FFT performance due to optimized radix-2 algorithms)
    fft_len = 1
    while fft_len < out_len:
        fft_len <<= 1  # Equivalent to fft_len *= 2
    
    # Compute FFTs of both sequences, zero-padded to fft_len
    X = fft(x, fft_len)
    Y = fft(y, fft_len)
    
    # Multiply in frequency domain (element-wise)
    result = ifft(X * Y)  # Result is complex if inputs are complex
    
    # Truncate to the correct linear convolution length
    return result[:out_len]
    
    
