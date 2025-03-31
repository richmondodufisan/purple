import os
import math
import csv
import re

def calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, freq, pump_power):


    if (N_layers != 3):
        raise RuntimeError("Error: This is for 3 Layer systems only")

    input_file = "FDTR_Three_Layer.i"
    temp_file = "FDTR_Three_Layer_temp.i"
    
    h1 = float(layer_props[2][0] * 1e6)
    kappa_z1 = layer_props[2][1] * 1e-6
    kappa_r1 = layer_props[2][2] * 1e-6
    rho1 = layer_props[2][3] * 1e-18
    c1 = layer_props[2][4]
    
    G_12 = interface_props[1] * 1e-12
    
    h2 = float(layer_props[1][0] * 1e6)
    kappa_z2 = layer_props[1][1] * 1e-6
    kappa_r2 = layer_props[1][2] * 1e-6
    rho2 = layer_props[1][3] * 1e-18
    c2 = layer_props[1][4]
    
    G_23 = interface_props[0] * 1e-12
    
    h3 = float(layer_props[0][0] * 1e6)
    kappa_z3 = layer_props[0][1] * 1e-6
    kappa_r3 = layer_props[0][2] * 1e-6
    rho3 = layer_props[0][3] * 1e-18
    c3 = layer_props[0][4]
    
    # Dictionary to map the variable names in the input file to the function arguments
    replacements = {
        'freq_val': freq,
    
        'transducer_thickness': h1,
        'k_trans_z': kappa_z1,
        'k_trans_r': kappa_r1,
        'rho_trans': rho1,
        'c_trans': c1,
        
        'sample_thickness_2': h2,
        'k_samp_z_2': kappa_z2,
        'k_samp_r_2': kappa_r2,
        'rho_samp_2': rho2,
        'c_samp_2': c2,
        
        'sample_thickness_3': h3,
        'k_samp_z_3': kappa_z3,
        'k_samp_r_3': kappa_r3,
        'rho_samp_3': rho3,
        'c_samp_3': c3,
    
        'pump_radius': r_pump * 1e6,
        'probe_radius': r_probe * 1e6,
        'pump_power': pump_power,
        
        'conductance_12': G_12,

        'conductance_23': G_23 
    }
    
    # Read the input file and modify the necessary lines
    with open(input_file, 'r') as file:
        lines = file.readlines()
    
    # Open a new file to write the modified content
    with open(temp_file, 'w') as file:
        for line in lines:
            for key, value in replacements.items():
                if key in line:
                    # Replace the value in the line
                    line = re.sub(rf"{key} = \S+", f"{key} = {value}", line)
            file.write(line)
    
    # Step 2: Run the simulation and suppress the console output
    os.system(f"../../purple-opt -i {temp_file} > output_log.txt 2>&1")
    
    # Step 3: Read the results from the generated CSV file
    output_csv = "FDTR_Three_Layer_Concentric_out.csv"
    
    
    
    H_imag = None
    H_real = None
    
    with open(output_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header

        # Read the entire CSV file and choose the last row
        rows = list(csv_reader)
        last_row = rows[-1]  # Get the last row

        H_imag = float(last_row[1])
        H_real = float(last_row[2])
    
    # Step 4: Check for division by zero and calculate phase and amplitude
    if H_real != 0:
        phase = math.atan(H_imag / H_real)
    else:
        phase = math.pi / 2 if H_imag > 0 else -math.pi / 2
    
    amplitude = math.sqrt(H_real**2 + H_imag**2)
    
    # Clean files
    os.system(f"rm FDTR_Three_Layer_temp*")
    
    return phase, amplitude
