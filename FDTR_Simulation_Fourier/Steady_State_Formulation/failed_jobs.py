# def get_failed_scripts(input_file, failed_indices):
    # with open(input_file, 'r') as f:
        # scripts = [line.strip() for line in f.readlines()]
    
    # failed_scripts = {idx: scripts[idx] for idx in failed_indices if idx < len(scripts)}
    
    # for idx, script in failed_scripts.items():
        # print(f"Job {idx}: {script}")

# # Example usage:
# failed_jobs = [5, 6, 98, 106, 112, 134, 156]  # Replace with actual failed indices
# input_file = "SteadyStateFourier.txt"  # Replace with the actual file containing script names

# get_failed_scripts(input_file, failed_jobs)



def find_job_line(filename, job_array_file="SteadyStateFourier_old.txt"):
    try:
        with open(job_array_file, "r") as file:
            lines = file.readlines()
            
            for index, line in enumerate(lines, start=1):  # Start counting from 1
                if filename.strip() == line.strip():
                    return index
        
        return f"File '{filename}' not found in {job_array_file}."
    except FileNotFoundError:
        return f"Job array file '{job_array_file}' not found."

# Example usage
script_name = "FDTR_input_GibbsExcess_StepFunction_BesselRing_Fourier_Steady_theta_0_freq_6e6_x0_-20.i"
line_number = find_job_line(script_name)
print(f"{script_name} is at line: {line_number}")


