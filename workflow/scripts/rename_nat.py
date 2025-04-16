import os
import argparse

# Set up argparse to handle command-line arguments
def main():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Rename files in the folder by shortening the file names.")
    
    # Add a required argument for the input folder path
    parser.add_argument('folder_path', type=str, help="Path to the folder containing the files to rename.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Folder path from the command-line argument
    folder_path = args.folder_path
    
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return

    # Iterate over all the files in the directory
    for filename in os.listdir(folder_path):
        # Check if the file is a .pdb file
        if filename.endswith('.pdb'):
            # Find the index of ' RecName:' in the filename (if it exists)
            if ' RecName:' in filename:
                # Extract the part before ' RecName:' and retain the file extension
                new_filename = filename.split(' RecName:')[0] + '.pdb'
                
                # Create the full path for the current and new filenames
                current_filepath = os.path.join(folder_path, filename)
                new_filepath = os.path.join(folder_path, new_filename)
                
                # Rename the file
                os.rename(current_filepath, new_filepath)
                print(f'Renamed: {filename} -> {new_filename}')

if __name__ == "__main__":
    main()