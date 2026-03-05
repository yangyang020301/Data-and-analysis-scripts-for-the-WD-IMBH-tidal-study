import numpy as np
from scipy.interpolate import interp1d

# Utility function: pad array B to match the length of array A, centering the data
def compute_coeff_3(mino_time, tau_of_mino_time, upsilon_r_orbit, Compression_Index,
                    Sigma_average, tt, t1, N):
    """Compute Coefficient_tau_lambda_Fourier3"""
    
    # Construct the complex exponential signal with radial orbital frequency
    f = np.exp(-1j * upsilon_r_orbit / Compression_Index *
               (mino_time - tau_of_mino_time / Sigma_average))
    
    # Interpolate the signal onto the target time grid t1 using cubic interpolation,
    # with extrapolation enabled beyond the original domain
    mino_tau_fourier_func = interp1d(tt, f, kind='cubic', fill_value='extrapolate')
    del f  # Free memory
    f = mino_tau_fourier_func(t1)
    t = t1

    # Check whether the time grid includes the 2π endpoint (typical for periodic signals)
    for iiiiii in range(1):
        if np.isclose(t[-1], 2 * np.pi, atol=1e-8):
            
            # Also check if the grid starts at 0
            if np.isclose(t[0], 0, atol=1e-8):
                t_use = t[:-1]  # Remove the duplicate 2π point to avoid aliasing
                f_use = f[:-1]  # Corresponding signal values
                N = len(t_use)
            else:
                # Keep the full array as-is (not ideal for periodic FFT)
                t_use = t
                f_use = f
                N = len(t_use)
        else:
            # Use the entire array unchanged
            t_use = t
            f_use = f
            N = len(t_use)
        
        # Check if the time grid is uniformly spaced
        dt = t_use[1] - t_use[0]
        is_uniform = np.allclose(np.diff(t_use), dt, rtol=1e-10)

        # ========================================================
        # 1. Compute the raw (unshifted) FFT, normalized by the number of points N
        f_n = np.fft.fft(f_use) / N
        
        # Generate standard frequency indices: n = 0, 1, ..., N-1
        # For a signal sampled over [0, 2π), the Fourier modes are integer-valued.
        # To represent negative frequencies, we will apply fftshift below.
        n_unshifted = np.arange(N)
        
        # Map indices to symmetric range around zero:
        #   e.g., [-N//2, ..., N//2 - 1] for even N,
        #         [-(N-1)//2, ..., (N-1)//2] for odd N
        n_unshifted = np.where(n_unshifted > N // 2, n_unshifted - N, n_unshifted)

        # ========================================================
        # 2. Shift the FFT so that zero frequency is centered:
        # negative frequencies on the left, positive on the right
        f_n_shifted = np.fft.fftshift(f_n)
        n_shifted = np.fft.fftshift(n_unshifted.astype(int))  # Enforce integer dtype

        # ========================================================
        # 3. Verify that the frequency indices are (numerically) integers
        if np.allclose(n_shifted, np.rint(n_shifted), atol=1e-10):
            n_final = n_shifted.astype(int)
        else:
            n_final = n_shifted
            
    # Return the reversed shifted Fourier coefficients
    # (common convention in some gravitational-wave or orbital dynamics codes)
    return f_n_shifted[::-1]
    
    
