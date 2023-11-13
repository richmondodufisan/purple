#!/bin/bash

# Check if the user provided both old and new app names
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <old_app_name> <new_app_name>"
    exit 1
fi

old_app_name="$1"
new_app_name="$2"

# Check if the directory exists
directory="/home/richmond98/projects/purple/FDTR_Simulation_Hydrodynamics/Kernels_and_Headers"  # Replace with the actual path to your directory
if [ ! -d "$directory" ]; then
    echo "Error: Directory not found!"
    exit 1
fi

# Go into the directory
cd "$directory" || exit 1

# Iterate through each file in the directory
for file in *; do
    if [ -f "$file" ]; then
	
		# Get object name
		filename=$(echo "$file" | sed 's/\.[^\.]*$//')
	
		if grep -q "registerMooseObject(\"${old_app_name}App\", ${filename});" "$file"; then
			
		
			# Use sed to replace the old app name with the new app name within the file content
			sed -i "s/registerMooseObject(\"${old_app_name}App\", ${filename});/registerMooseObject(\"${new_app_name}App\", ${filename});/g" "$file"
			echo "Replaced in file: $file"
		fi
    fi
done

echo "Replacement complete."
