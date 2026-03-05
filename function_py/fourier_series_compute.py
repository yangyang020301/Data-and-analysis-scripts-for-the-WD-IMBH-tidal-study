import numpy as np 


def fourier_series_compute_function(args):
    """
    Worker function executed by a subprocess to compute Fourier coefficients for a single task.
    All required data must be passed via `args` to ensure compatibility with multiprocessing.
    
    Parameters
    ----------
    args : tuple
        A tuple containing (t, f, N), where:
        - t: time or phase grid (array_like)
        - f: complex-valued signal sampled on t (array_like)
        - N: expected number of points (may be updated internally)
        
    Returns
    -------
    Coeff_Four : ndarray
        Reversed shifted Fourier coefficients (complex), ordered from highest positive 
        to most negative mode (common convention in orbital dynamics).
    """
    t, f, N = args

    # Check if the grid includes the 2π endpoint (typical for periodic signals)
    if np.isclose(t[-1], 2 * np.pi, atol=1e-8):
        # Also check if the grid starts at 0
        if np.isclose(t[0], 0, atol=1e-8):
            t_use = t[:-1]  # Remove the duplicate 2π point to avoid aliasing
            f_use = f[:-1]  # Corresponding signal values
            N = len(t_use)
        else:
            # Keep full array as-is (not ideal for periodic FFT)
            t_use = t
            f_use = f
            N = len(t_use)
    else:
        t_use = t
        f_use = f
        N = len(t_use)

    # Check if the time/phase grid is uniformly spaced
    dt = t_use[1] - t_use[0]
    is_uniform = np.allclose(np.diff(t_use), dt, rtol=1e-10)

    # ==========================================================
    # 1. Compute raw (unshifted) FFT, normalized by N
    # ==========================================================
    f_n = np.fft.fft(f_use) / N
    
    # Generate standard frequency indices: n = 0, 1, ..., N-1
    # For a signal on [0, 2π), Fourier modes are integer-valued.
    # To represent negative frequencies, we apply fftshift below.
    n_unshifted = np.arange(N)
    
    # Map indices to symmetric range around zero:
    #   e.g., [-N//2, ..., N//2 - 1] for even N
    n_unshifted = np.where(n_unshifted > N // 2, n_unshifted - N, n_unshifted)

    # ==========================================================
    # 2. Shift FFT so zero frequency is centered:
    #    negative frequencies on the left, positive on the right
    # ==========================================================
    f_n_shifted = np.fft.fftshift(f_n)
    n_shifted = np.fft.fftshift(n_unshifted.astype(int))  # Enforce integer dtype

    # ==========================================================
    # 3. Verify that frequency indices are (numerically) integers
    # ==========================================================
    if np.allclose(n_shifted, np.rint(n_shifted), atol=1e-10):
        n_final = n_shifted.astype(int)
    else:
        n_final = n_shifted

    # ==========================================================
    # 4. Create a list of (mode, coefficient) pairs
    # ==========================================================
    fourier_table = list(zip(n_final, f_n_shifted))

    # ==========================================================
    # 5. Convert to NumPy structured array for convenient indexing
    # ==========================================================
    dtype = [('n', int), ('coeff', complex)]
    table_array = np.array(list(zip(n_final, f_n_shifted)), dtype=dtype)

    # ==========================================================
    # 6. Prepare output: reversed shifted coefficients
    # ==========================================================
    Coeff_Four = f_n_shifted  # Original variable name preserved
    Coeff_Four = Coeff_Four[::-1]  # Reverse order (e.g., +max → 0 → -max)

    return Coeff_Four
    
    
    
    
