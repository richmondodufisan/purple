import os
import math
import csv
import re

def calc_thermal_response(N_layers, layer_props, interface_props, r_pump, r_probe, freq, pump_power):
    # Step 1: Modify the input file
    input_file = "FDTR_Two_Layer.i"
    temp_file = "FDTR_Two_Layer_temp.i"
    
    h1 = layer_props[0][0]
    kappa_z1 = layer_props[0][1]
    kappa_r1 = layer_props[0][2]
    rho1 = layer_props[0][3]
    c1 = layer_props[0][4]
    
    G_au_si = interface_props[0]
    
    h2 = layer_props[1][0]
    kappa_z2 = layer_props[1][1]
    kappa_r2 = layer_props[1][2]
    rho2 = layer_props[1][3]
    c2 = layer_props[1][4]
    
    # Dictionary to map the variable names in the input file to the function arguments
    replacements = {
        'transducer_thickness': h1
        'k_trans_z': kappa_z1
        'k_trans_r': kappa_r1
    
    
        'pump_radius': r_pump,
        'N_layers': N_layers,
        'layer_props': layer_props,
        'au_si_conductance_positive': interface_props[0],
        'probe_radius': r_probe,
        'punp_radius': r_pump
        'freq_val': freq,
        'pump_power': pump_power
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
    output_csv = "FDTR_Two_Layer_out.csv"
    H_imag = None
    H_real = None
    
    with open(output_csv, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header
        second_row = next(csv_reader)  # Get the second row
        H_imag = float(second_row[1])
        H_real = float(second_row[2])
    
    # Step 4: Calculate phase and amplitude
    phase = math.atan(H_imag / H_real)
    amplitude = math.sqrt(H_real**2 + H_imag**2)
    
    # Return the phase and amplitude
    return phase, amplitude
