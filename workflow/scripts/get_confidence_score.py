import os
import argparse

def extract_confidence_score(pdb_file):
    """
    Function to extract the confidence score from a PDB file.
    This assumes that the confidence score is stored in a line starting with 'REMARK  CONF:'
    """
    confidence_score = None
    
    with open(pdb_file, 'r') as file:
        for line in file:
            # Check for lines starting with 'REMARK  CONF:'
            if line.startswith("REMARK  CONF:"):
                # Extract the confidence score, which is after "REMARK  CONF:"
                confidence_score = float(line.split(":")[1].strip())
                break
                
    return confidence_score

def process_pdb_files(input_directory, output_file):
    """
    Process all PDB files in the given directory, extract their confidence scores,
    and write the results to an output file.
    """
    with open(output_file, 'w') as out_file:
        out_file.write("PDB Filename\tConfidence Score\n")  # Write header
        
        for pdb_filename in os.listdir(input_directory):
            if pdb_filename.endswith(".pdb"):  # Only process PDB files
                pdb_path = os.path.join(input_directory, pdb_filename)
                confidence_score = extract_confidence_score(pdb_path)
                
                if confidence_score is not None:
                    out_file.write(f"{pdb_filename}\t{confidence_score}\n")
                else:
                    out_file.write(f"{pdb_filename}\tNo confidence score found\n")

    print(f"Processed files and saved the results in {output_file}")

def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(description="Process PDB files and extract their confidence scores.")
    
    # Add arguments
    parser.add_argument('input_directory', type=str, help="Directory containing PDB files.")
    parser.add_argument('output_file', type=str, help="Output file to save the results.")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Process the PDB files based on the input directory and output file provided by the user
    process_pdb_files(args.input_directory, args.output_file)

if __name__ == "__main__":
    main()
