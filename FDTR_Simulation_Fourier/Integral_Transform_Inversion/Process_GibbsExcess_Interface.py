import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import glob
from scipy.interpolate import interp1d
from scipy.integrate import trapz

freq_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]  # MHz
flux_normals = []
temp_jumps = []



for i, freq in enumerate(freq_list):
    print(f"\n--- Processing frequency: {freq} MHz ---")
    freq_dir = f"./paper_results/Interface_5um/{freq}MHz"

    def load_flux_profile(direction):
        files = sorted(glob.glob(f"{freq_dir}/*flux_profile_{direction}_*_0001.csv"))
        combined = []
        for f in files:
            df = pd.read_csv(f, skiprows=1, header=None)
            flux = df.iloc[:, 0]
            x = df.iloc[:, 2]
            combined.append(pd.DataFrame({"x": x, "flux": flux}))
        full_df = pd.concat(combined)
        full_df = full_df.sort_values(by="x")
        return full_df["x"].values, full_df["flux"].values

    x_pos, flux_x = load_flux_profile("x")
    _, flux_y = load_flux_profile("y")
    _, flux_z = load_flux_profile("z")

    x_si = x_pos * 1e-6
    x_down = np.arange(-30e-6, 31e-6, 1e-6)

    interp_fx_raw = interp1d(x_si, flux_x, kind='linear', fill_value="extrapolate")
    interp_fy_raw = interp1d(x_si, flux_y, kind='linear', fill_value="extrapolate")
    interp_fz_raw = interp1d(x_si, flux_z, kind='linear', fill_value="extrapolate")

    flux_x_down_raw = interp_fx_raw(x_down)
    flux_y_down_raw = interp_fy_raw(x_down)
    flux_z_down_raw = interp_fz_raw(x_down)
    


    epsilon = 0.00001e-6
    integration_step = 0.1e-6
    x_integrate = np.arange(-epsilon, epsilon + integration_step, integration_step)
    flux_x_integrate = interp_fx_raw(x_integrate)
    integrated_flux = np.trapz(flux_x_integrate, x_integrate)
    flux_normal = integrated_flux / (2 * epsilon)
    print(f"Flux normal at interface: {flux_normal:.3f} W/m²")

    flux_x_down_scaled = flux_x_down_raw / flux_normal
    flux_y_down_scaled = flux_y_down_raw / flux_normal
    flux_z_down_scaled = flux_z_down_raw / flux_normal

    # Only plot for first frequency
    if i == 0:
        plt.figure(figsize=(10, 6))
        plt.plot(x_down * 1e6, flux_x_down_raw, label="Flux X (raw)")
        plt.plot(x_down * 1e6, flux_y_down_raw, label="Flux Y (raw)")
        plt.plot(x_down * 1e6, flux_z_down_raw, label="Flux Z (raw)")
        plt.xlabel("X Position (µm)")
        plt.ylabel("Flux Magnitude (W/m²)")
        plt.title(f"Raw Flux Profiles (Freq: {freq} MHz)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"flux_profiles_raw_{freq}MHz.png")
        plt.show()

        plt.figure(figsize=(10, 6))
        plt.plot(x_down * 1e6, flux_x_down_scaled, label="Flux X (scaled)")
        plt.plot(x_down * 1e6, flux_y_down_scaled, label="Flux Y (scaled)")
        plt.plot(x_down * 1e6, flux_z_down_scaled, label="Flux Z (scaled)")
        plt.xlabel("X Position (µm)")
        plt.ylabel("Flux Magnitude (normalized)")
        plt.title(f"Scaled Flux Profiles (Freq: {freq} MHz)")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"flux_profiles_scaled_{freq}MHz.png")
        plt.show()

    # Load and interpolate conductivity
    cond_profile = pd.read_csv("./paper_results/Interface_5um/Thermal_Conductivity_Profile_GibbsExcess_Interface_SuperGaussianRing_5um_out_theta_0.csv")
    x_kappa = cond_profile["Position (µm)"].values * 1e-6
    kappa_r = cond_profile["Kappa_r (W/m·K)"].values
    kappa_z = cond_profile["Kappa_z (W/m·K)"].values

    interp_kappa_r = interp1d(x_kappa, kappa_r, kind='linear', fill_value="extrapolate")
    interp_kappa_z = interp1d(x_kappa, kappa_z, kind='linear', fill_value="extrapolate")

    kappa_r_interp_vals = interp_kappa_r(x_down)
    kappa_z_interp_vals = interp_kappa_z(x_down)
    
    
    # Get bulk values far from interface (leftmost point)
    # kappa_r_bulk = kappa_r_interp_vals[0]
    # kappa_z_bulk = kappa_z_interp_vals[0]

    # inv_kappa_r_bulk = 1.0 / kappa_r_bulk
    # inv_kappa_z_bulk = 1.0 / kappa_z_bulk

    # print(f"Bulk κ_r = {kappa_r_bulk:.4f}, 1/κ_r = {inv_kappa_r_bulk:.4e} m·K/W")
    # print(f"Bulk κ_z = {kappa_z_bulk:.4f}, 1/κ_z = {inv_kappa_z_bulk:.4e} m·K/W")


    flux_r_down_raw = np.sqrt(flux_x_down_raw**2 + flux_y_down_raw**2)
    term1 = (flux_r_down_raw**2) / kappa_r_interp_vals + (flux_z_down_raw**2) / kappa_z_interp_vals

    if i == 0:
        plt.figure(figsize=(10, 6))
        plt.plot(x_down * 1e6, term1, color="blue")
        plt.xlabel("X Position (µm)")
        plt.ylabel(r"$\kappa^{-1}_{\mathrm{loc}} : (\mathbf{q} \otimes \mathbf{n})$ [W/m²/K]")
        plt.title(f"Dissipation Profile (Freq: {freq} MHz)")
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(f"local_dissipation_{freq}MHz.png")
        plt.show()

    # Integrate
    RB_numerator = np.trapz(term1, x_down)


    flux_normals.append(flux_normal)

    temp_jumps.append(RB_numerator)

    print(f"Temperature Jump at {freq} MHz: {RB_numerator:.4e} K")

# Convert to arrays
flux_normals = np.array(flux_normals)
temp_jumps = np.array(temp_jumps)



# Fit with intercept
R_B_fit, intercept = np.polyfit(flux_normals, temp_jumps, deg=1)
fit_line = R_B_fit * flux_normals + intercept

plt.figure(figsize=(8, 6))
plt.plot(flux_normals, temp_jumps, 'o', label='Data Points')
plt.plot(flux_normals, fit_line, '-', color='red', label=fr'Fit: $R_B$ = {R_B_fit:.2e}, Intercept = {intercept:.2e}')
plt.xlabel("Flux Normal, q_GB (W/m²)", fontsize=13)
plt.ylabel("Temperature Jump (K)", fontsize=13)

# plt.yscale('log')

plt.title("Temperature Jump vs Flux Normal", fontsize=14)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("RB_fit_flux_vs_tempjump.png")
plt.show()

print("===================================================")
print(f"Fitted Grain Boundary Resistance R_B: {R_B_fit:.4e} m²·K/W")
print(f"Intercept: {intercept:.4e} K")
print("===================================================")
