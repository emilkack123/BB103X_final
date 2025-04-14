import os
import subprocess

input_dir = 'results/nat/'
output_dir = 'results/converted_pdbqt_natural/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for filename in os.listdir(input_dir):
    if filename.endswith('.pdb'):
        input_file = os.path.join(input_dir, filename)
        output_file = os.path.join(output_dir, filename.replace('.pdb', '.pdbqt'))

        command = [
            'prepare_receptor4.py', 
            '-r', input_file,
            '-o', output_file
        ]

        try:
            subprocess.check_call(command)
            print("Successfully converted {} to PDBQT.".format(filename))
        except subprocess.CalledProcessError as e:
            print("Error processing {}: {}".format(filename, e))
