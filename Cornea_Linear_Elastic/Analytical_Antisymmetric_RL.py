import numpy as np
import cmath

def calc_dispersion_relation(thickness, density, poissons_ratio, shear_modulus, freq_min, freq_max, num_points):
    # Derived material properties
    h_half = thickness / 2
    c_T = np.sqrt(shear_modulus / density)
    lame_lambda = (2 * shear_modulus * poissons_ratio) / (1 - (2 * poissons_ratio))
    c_L = np.sqrt((lame_lambda + (2 * shear_modulus)) / density)

    # Define frequency range
    freq_range = np.linspace(freq_min, freq_max, num_points)

    # Dispersion relation function returning the magnitude
    def D_cp(w, c_T, c_L, c_phase, h):
        k = (w / c_phase)  # wave number, k
        q = cmath.sqrt((w**2) / (c_T**2) - k**2)
        p = cmath.sqrt((w**2) / (c_L**2) - k**2)

        LHS_term = (cmath.tan(q * h)) / (cmath.tan(p * h))
        RHS_term = -(((q**2) - (k**2))**2) / (4 * (k**2) * p * q)

        D = LHS_term - RHS_term
        return D.real

    # Bracketing and Bisection parameters
    cp_min, cp_max = 0.1, 50  # Range for phase velocities
    jump = 0.05                 # Step size for bracketing
    tolerance = 1e-8            # Tolerance for bisection convergence

    # Initialize lists to store frequencies and corresponding phase velocities
    frequencies = []
    phase_velocities = []

    # Loop over each frequency to calculate D(cp) and find roots
    for freq in freq_range:
        w = 2 * np.pi * freq  # Angular frequency for this iteration
        cp_roots = []  # To store phase velocities (roots) for each frequency

        # Bracketing: Find intervals where sign change occurs
        cp1 = cp_min
        while cp1 < cp_max:
            cp2 = cp1 + jump
            f1val = D_cp(w, c_T, c_L, cp1, h_half)
            f2val = D_cp(w, c_T, c_L, cp2, h_half)

            if f1val * f2val < 0:  # Sign change indicates a potential root
                # Bisection method within the interval [cp1, cp2]
                while (cp2 - cp1) > tolerance:
                    cp_mid = (cp1 + cp2) / 2
                    f_mid = D_cp(w, c_T, c_L, cp_mid, h_half)

                    if f1val * f_mid < 0:
                        cp2 = cp_mid
                        f2val = f_mid
                    elif f2val * f_mid < 0:
                        cp1 = cp_mid
                        f1val = f_mid
                    else:
                        break  # If f_mid is close enough to zero

                cp_roots.append((cp1 + cp2) / 2)

            cp1 = cp2  # Move to the next bracket interval

        # Store results for each frequency
        frequencies.extend([freq] * len(cp_roots))
        phase_velocities.extend(cp_roots)

    return frequencies, phase_velocities
