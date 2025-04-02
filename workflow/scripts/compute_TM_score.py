import os
import pandas as pd
import glob
import argparse

def get_best_reference(confidence_scores_file, nat_folder):
    """
    Selects the natural sequence with the highest confidence score from results/confidence_scores.csv
    and returns its corresponding PDB file path by searching for the sequence name in the title.
    """
    df = pd.read_csv(confidence_scores_file)
    best_seq = df.loc[df['STABILITY'].idxmax(), 'ID']  # Get the sequence name with highest score
    
    # Search for a PDB file that contains the sequence name in its filename
    pdb_files = glob.glob(os.path.join(nat_folder, "*.pdb"))
    for pdb_file in pdb_files:
        if best_seq in os.path.basename(pdb_file):
            return pdb_file
    
    raise FileNotFoundError(f"No reference PDB file found in {nat_folder} containing {best_seq} in the title.")

def calculate_tm_score(reference_pdb, target_pdb):
    """
    Computes the TM-score between the reference PDB file and a target PDB file.
    Assumes an external TM-score tool (e.g., TM-align) is installed and available in PATH.
    """
    tm_align_exec = "./TMalign"  # Change this if necessary
    output_file = "tm_output.txt"
    
    cmd = f'{tm_align_exec} "{target_pdb}" "{reference_pdb}" > {output_file}'
    os.system(cmd)  # Run TM-align
    
    # Extract TM-score from the output file
    with open(output_file, "r") as file:
        for line in file:
            if "TM-score=" in line:
                return float(line.split()[1])
    
    return None  # Return None if TM-score not found

def process_pdb_files(gen_folder, reference_pdb, output_csv):
    """
    Computes TM-scores for all generated PDB files against the reference PDB and saves to CSV.
    """
    data = {"ID": [], "TM_SCORE": []}
    pdb_files = glob.glob(os.path.join(gen_folder, "*.pdb"))
    
    if not pdb_files:
        print(f"No PDB files found in {gen_folder}")
        return
    
    for pdb_file in pdb_files:
        seq_id = os.path.basename(pdb_file).split(".pdb")[0]  # Extract sequence name
        tm_score = calculate_tm_score(reference_pdb, pdb_file)
        
        if tm_score is not None:
            data["ID"].append(seq_id)
            data["TM_SCORE"].append(tm_score)
    
    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"TM-scores saved to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Calculate TM-score for generated PDB files.")
    parser.add_argument("--confidence_scores", default="results/confidence_scores.csv", 
                        help="CSV file with confidence scores (default: results/confidence_scores.csv)")
    parser.add_argument("--gen_folder", default="results/gen", 
                        help="Folder containing generated PDB files (default: results/gen)")
    parser.add_argument("--nat_folder", default="results/nat", 
                        help="Folder containing natural PDB files (default: results/nat)")
    parser.add_argument("--output", default="results/tm_scores.csv", 
                        help="Path to save the output CSV file (default: tm_scores.csv)")
    
    args = parser.parse_args()
    
    reference_pdb = get_best_reference(args.confidence_scores, args.nat_folder)
    process_pdb_files(args.gen_folder, reference_pdb, args.output)

if __name__ == "__main__":
    main()
