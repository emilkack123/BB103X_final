import os
import argparse
import csv
import shutil

def main():
    parser = argparse.ArgumentParser(description="Copy and rename .pdb files from the folder, saving them in a new directory.")
    parser.add_argument('folder_path', type=str, help="Path to the folder containing the files to process.")
    parser.add_argument('log_path', type=str, help="Path to save the CSV log of renamed files.")  # New argument
    args = parser.parse_args()

    folder_path = args.folder_path
    log_path = args.log_path

    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Ensure output directory exists
    output_dir = os.path.dirname(log_path)
    os.makedirs(output_dir, exist_ok=True)

    # Copy and rename files
    with open(log_path, mode='w', newline='') as log_file:
        writer = csv.writer(log_file)
        writer.writerow(["Original Filename", "New Filename"])  # Header row

        for filename in os.listdir(folder_path):
            if filename.endswith('.pdb') and ' RecName:' in filename:
                new_filename = filename.split(' RecName:')[0] + '.pdb'
                source_path = os.path.join(folder_path, filename)
                destination_path = os.path.join(output_dir, new_filename)

                shutil.copy2(source_path, destination_path)
                print(f'Copied and renamed: {filename} -> {new_filename}')

                writer.writerow([filename, new_filename])

if __name__ == "__main__":
    main()