def get_failed_scripts(input_file, failed_indices):
    with open(input_file, 'r') as f:
        scripts = [line.strip() for line in f.readlines()]
    
    failed_scripts = {idx: scripts[idx] for idx in failed_indices if idx < len(scripts)}
    
    for idx, script in failed_scripts.items():
        print(f"Job {idx}: {script}")

# Example usage:
failed_jobs = [5, 6, 98, 106, 112, 134, 156]  # Replace with actual failed indices
input_file = "SteadyStateFourier.txt"  # Replace with the actual file containing script names

get_failed_scripts(input_file, failed_jobs)
