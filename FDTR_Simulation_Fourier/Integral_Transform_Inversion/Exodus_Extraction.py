import pyvista as pv
import numpy as np
import matplotlib.pyplot as plt

# Load Exodus file
filename = "./paper_results/Interface_5um/FDTR_input_GibbsExcess_Interface_SuperGaussianRing_Fourier_Steady_theta_0_freq_1e6_x0_0_out.e"
dataset = pv.read(filename)

# Recursively extract all unstructured grids
def extract_grids(multiblock):
    grids = []
    for i in range(multiblock.n_blocks):
        block = multiblock[i]
        if isinstance(block, pv.UnstructuredGrid):
            grids.append(block)
        elif isinstance(block, pv.MultiBlock):
            grids.extend(extract_grids(block))
    return grids

# Extract grids
grids = extract_grids(dataset)
left_grid = grids[1]
right_grid = grids[2]

# Function to slice and interpolate
def slice_and_extract_flux(grid, flux_var, z_val, x_min, x_max):
    # Slice first
    sliced = grid.slice(normal='z', origin=(0, 0, z_val))

    # Interpolate flux to points on the slice
    sliced_interp = sliced.cell_data_to_point_data()
    
    if flux_var not in sliced_interp.point_data:
        print(f"⚠️ Variable '{flux_var}' not in point_data after interpolation.")
        return np.array([]), np.array([])

    x_vals = sliced_interp.points[:, 0]
    flux_vals = sliced_interp.point_data[flux_var]

    # Filter in x-direction
    mask = (x_vals >= x_min) & (x_vals <= x_max)
    return x_vals[mask], flux_vals[mask]

# Parameters
z_val = -1.0  # micron
x_range = (-30, 30)

# Get both sides
x_left, flux_left = slice_and_extract_flux(left_grid, "flux_x_left", z_val, x_range[0], 0)
x_right, flux_right = slice_and_extract_flux(right_grid, "flux_x_right", z_val, 0, x_range[1])

# Merge and sort
x_all = np.concatenate([x_left, x_right]) * 1e6  # Convert to µm
flux_all = np.concatenate([flux_left, flux_right])
sort_idx = np.argsort(x_all)

# Plot
plt.figure(figsize=(10, 6))
plt.plot(x_all[sort_idx], flux_all[sort_idx], '.', label=f"Flux X at z = {z_val} µm")
plt.xlabel("X Position (µm)")
plt.ylabel("Flux X (W/m²)")
plt.title(f"Flux X Profile at z = {z_val} µm")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("flux_x_slice_corrected.png")
plt.show()
















# import pyvista as pv

# filename = "./paper_results/Interface_5um/FDTR_input_GibbsExcess_Interface_SuperGaussianRing_Fourier_Steady_theta_0_freq_1e6_x0_0_out.e"  # update if needed
# dataset = pv.read(filename)

# print("🧩 Blocks in the Exodus file:\n")
# for i, block in enumerate(dataset):
    # print(f"Block {i}: Type = {type(block)}")
    # if isinstance(block, pv.UnstructuredGrid):
        # print(f"  - Number of points: {block.n_points}")
        # print(f"  - Point data arrays: {list(block.point_data.keys())}")
    # else:
        # print("  - Not an UnstructuredGrid, skipping.")
    # print()



# import pyvista as pv

# def extract_grids(multiblock):
    # """Recursively extract UnstructuredGrids from a MultiBlock dataset."""
    # grids = []
    # for i in range(multiblock.n_blocks):
        # block = multiblock[i]
        # if isinstance(block, pv.UnstructuredGrid):
            # grids.append(block)
        # elif isinstance(block, pv.MultiBlock):
            # grids.extend(extract_grids(block))
    # return grids

# filename = "./paper_results/Interface_5um/FDTR_input_GibbsExcess_Interface_SuperGaussianRing_Fourier_Steady_theta_0_freq_1e6_x0_0_out.e"  # Update path if needed
# dataset = pv.read(filename)

# print("🔍 Extracting actual mesh blocks...\n")
# grids = extract_grids(dataset)

# for i, grid in enumerate(grids):
    # print(f"Grid {i}:")
    # print(f"  - Number of points: {grid.n_points}")
    # print(f"  - Point data: {list(grid.point_data.keys())}")
    # print(f"  - Bounds: {grid.bounds}\n")
    
    
    
    
# import pyvista as pv

# filename = "./paper_results/Interface_5um/FDTR_input_GibbsExcess_Interface_SuperGaussianRing_Fourier_Steady_theta_0_freq_1e6_x0_0_out.e"
# dataset = pv.read(filename)

# def extract_grids(multiblock):
    # grids = []
    # for i in range(multiblock.n_blocks):
        # block = multiblock[i]
        # if isinstance(block, pv.UnstructuredGrid):
            # grids.append(block)
        # elif isinstance(block, pv.MultiBlock):
            # grids.extend(extract_grids(block))
    # return grids

# grids = extract_grids(dataset)

# # Print available elemental variables (cell data)
# for i, grid in enumerate(grids):
    # print(f"\nGrid {i}:")
    # print(f"  - Number of cells: {grid.n_cells}")
    # print(f"  - Elemental data (cell_data): {list(grid.cell_data.keys())}")

