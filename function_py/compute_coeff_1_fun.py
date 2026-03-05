import numpy as np
from scipy.interpolate import interp1d

def compute_coeff_1(mino_time, tau_of_mino_time, Psi_mino_average, Compression_Index,
                    Sigma_average, tt, t1, N):
    """
    Compute Coefficient_tau_lambda_Fourier1.

    This function computes the Fourier coefficients of a complex exponential signal
    defined on a possibly non-uniform time grid, after interpolating it onto a uniform
    or near-uniform grid `t1`. It handles periodic boundary conditions by optionally
    removing the endpoint at 2π (if present) to avoid duplication in FFT computation.
    The resulting FFT is shifted so that zero frequency is centered, and the coefficient
    array is returned in reversed order (positive frequencies first, then negative).

    Parameters
    ----------
    mino_time : array_like
        Original time samples corresponding to the phase variable.
    tau_of_mino_time : array_like
        Time delay values evaluated at `mino_time`.
    Psi_mino_average : float
        Average value of the orbital phase (Psi).
    Compression_Index : float
        A scaling parameter used in the phase compression.
    Sigma_average : float
        Average value of the redshift factor (Sigma).
    tt : array_like
        Time points associated with the original signal for interpolation.
    t1 : array_like
        Target time grid for interpolation (typically uniform over [0, 2π]).
    N : int
        Expected number of points (may be updated internally if endpoint is removed).

    Returns
    -------
    f_n_shifted_reversed : ndarray
        Reversed version of the shifted FFT coefficients (i.e., ordered from highest
        positive mode down through zero to most negative mode). Complex-valued.
    """
    # Construct the complex exponential signal
    f = np.exp(-1j * Psi_mino_average / Compression_Index *
               (mino_time - tau_of_mino_time / Sigma_average))

    # Interpolate onto the target grid t1 using cubic interpolation with extrapolation
    mino_tau_fourier_func = interp1d(tt, f, kind='cubic', fill_value='extrapolate')
    del f  # Free memory
    f = mino_tau_fourier_func(t1)
    t = t1

    # Process the time grid for FFT compatibility
    for _ in range(1):  # Single-pass logic block (used for early exit via conditionals)
        # Check if the grid includes the 2π endpoint (periodic boundary)
        if np.isclose(t[-1], 2 * np.pi, atol=1e-8):
            # Also check if it starts at 0
            if np.isclose(t[0], 0, atol=1e-8):
                # Remove the duplicate 2π point to avoid aliasing in FFT
                t_use = t[:-1]
                f_use = f[:-1]
                N = len(t_use)
            else:
                # Keep full array, though this case is not ideal for periodic FFT
                t_use = t
                f_use = f
                N = len(t_use)
        else:
            # No 2π endpoint; use as-is
            t_use = t
            f_use = f
            N = len(t_use)

        # Check if the time grid is uniformly spaced
        dt = t_use[1] - t_use[0]
        is_uniform = np.allclose(np.diff(t_use), dt, rtol=1e-10)

        # ========================================================
        # 1. Compute raw FFT (unshifted), normalized by N
        f_n = np.fft.fft(f_use) / N

        # Generate unshifted frequency indices: 0, 1, ..., N-1
        n_unshifted = np.arange(N)
        # Map to symmetric range: [-N//2, ..., N//2 - 1] (or similar for odd N)
        n_unshifted = np.where(n_unshifted > N // 2, n_unshifted - N, n_unshifted)

        # ========================================================
        # 2. Shift FFT so that zero frequency is at the center
        f_n_shifted = np.fft.fftshift(f_n)
        n_shifted = np.fft.fftshift(n_unshifted.astype(int))  # Ensure integer dtype

        # ========================================================
        # 3. Validate that frequency indices are (numerically) integers
        if np.allclose(n_shifted, np.rint(n_shifted), atol=1e-10):
            n_final = n_shifted.astype(int)
        else:
            n_final = n_shifted

    # Return reversed shifted coefficients (common convention in some physics contexts)
    return f_n_shifted[::-1]
