from __future__ import print_function  # Ensures compatibility for print()

import os
import subprocess

# Define the input and output directories
input_dir = 'results/gen/'
output_dir = 'results/converted_pdbqt/'

# Make sure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop through all PDB files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('.pdb'):  # Only process PDB files
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename.replace('.pdb', '.pdbqt'))

        # Run the prepare_receptor4.py script for each file
        command = [
            'python2', '/home/moa/miniforge3/envs/bb103x/CCSBpckgs/AutoDockTools/Utilities24/prepare_receptor4.py',
            '-r', input_file, '-o', output_file
        ]
        
        # Execute the command
        try:
            subprocess.check_call(command)  # Use check_call instead of run
            print("Successfully converted {} to PDBQT.".format(filename))  # Using .format() for string formatting
        except subprocess.CalledProcessError as e:
            print("Error processing {}: {}".format(filename, e))  # Using .format() for string formatting
