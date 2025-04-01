import os
import pandas as pd
import glob
import argparse

def extract_confidence_score(pdb_file, is_nat=False):
    """
    Extracts confidence scores from a PDB file for CA (alpha carbon) atoms.
    Computes the mean confidence score as stability.
    Adjusts the ID format for 'nat' sequences (splits at space, then at '.').
    """
    scores = []
    pdb_filename = os.path.basename(pdb_file)  # Get filename

    if is_nat:
        clean_id = pdb_filename.split(" ")[0]  # Take first part before space
        pdb_id = clean_id.split(".pdb")[0]  # Take first part before dot
    else:
        pdb_id = pdb_filename.split(".")[0]  # Take first part before dot

    with open(pdb_file, "r") as file:
        for line in file:
            if line.startswith("ATOM") and " CA " in line:
                try:
                    confidence_score = float(line[61:66].strip())  # Extract confidence score (columns 62-66)
                    scores.append(confidence_score)
                except ValueError:
                    continue

    stability = sum(scores) / len(scores) if scores else 0  # Compute mean confidence score or default to 0

    return pdb_id, stability

def process_pdb_files(folders, output_csv):
    """
    Finds all PDB files in the given folders, extracts stability scores, and saves to CSV.
    """
    data = {"ID": [], "STABILITY": []}

    for folder in folders:
        pdb_files = glob.glob(os.path.join(folder, "*.pdb"))  # Find all PDB files in the folder
        is_nat = "nat" in folder.lower()  # Check if the folder is 'results/nat/'

        if not pdb_files:
            print(f"No PDB files found in {folder}")
            continue

        for pdb_file in pdb_files:
            pdb_id, stability = extract_confidence_score(pdb_file, is_nat)
            data["ID"].append(pdb_id)
            data["STABILITY"].append(stability)

    # Save to CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False)
    print(f"Stability scores saved to {output_csv}")

def main():
    parser = argparse.ArgumentParser(description="Extract stability scores from PDB files.")
    parser.add_argument("--folders", nargs="+", default=["results/gen", "results/nat"], 
                        help="Folders containing PDB files (default: results/gen and results/nat)")
    parser.add_argument("--output", default="stability_scores.csv", 
                        help="Path to save the output CSV file (default: stability_scores.csv)")
    
    args = parser.parse_args()
    process_pdb_files(args.folders, args.output)

if __name__ == "__main__":
    main()
