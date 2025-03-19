import subprocess
import argparse
import os

def run_clustal_omega(input_fasta, output_fasta, dist_matrix):
    """ Runs Clustal Omega to perform MSA and generate a distance matrix. """
    
    # Ensure Clustal Omega is installed
    clustalo_path = "clustalo"  # Change this if Clustal Omega is installed elsewhere

    # Step 1: Multiple Sequence Alignment (MSA)
    msa_command = [
        clustalo_path,
        "-i", input_fasta,
        "-o", output_fasta,
        "--auto",
        "--force"
    ]
    print(f"🚀 Running Clustal Omega MSA...\n{' '.join(msa_command)}")
    subprocess.run(msa_command, check=True)

    # Step 2: Compute Distance Matrix
    dist_command = [
        clustalo_path,
        "-i", input_fasta,
        "--distmat-out", dist_matrix,
        "--full",
        "--force"
    ]
    print(f"🚀 Computing Pairwise Distance Matrix...\n{' '.join(dist_command)}")
    subprocess.run(dist_command, check=True)

    print(f"✅ Distance matrix saved at: {dist_matrix}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a distance matrix using Clustal Omega")
    parser.add_argument("input_fasta", help="Path to input FASTA file (combined gen+nat)")
    parser.add_argument("output_fasta", help="Path to output aligned FASTA file")
    parser.add_argument("dist_matrix", help="Path to save the distance matrix")
    args = parser.parse_args()

    run_clustal_omega(args.input_fasta, args.output_fasta, args.dist_matrix)
