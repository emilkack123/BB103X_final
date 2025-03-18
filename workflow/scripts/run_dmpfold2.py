#!/usr/bin/env python3
import argparse
import os
import logging
import subprocess

def setup_logging():
    """ Konfigurerar loggning. """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

def run_dmpfold(input_file, output_file):
    """ Kör dmpfold på en ALN-fil och sparar output i PDB-format. """
    logging.info(f"🚀 Running dmpfold on {input_file}...")

    # Skapa output-katalogen om den inte finns
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    # Kör dmpfold
    result = subprocess.run(
        ["dmpfold", "-i", input_file, "-n", "0", "-m", "0"],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        logging.error(f"❌ Error running dmpfold on {input_file}: {result.stderr}")
        exit(1)

    # Spara resultatet till en PDB-fil
    with open(output_file, "w") as f:
        f.write(result.stdout)

    logging.info(f"✅ Model saved in {output_file}")

if __name__ == "__main__":
    setup_logging()

    parser = argparse.ArgumentParser(description="Run dmpfold on an ALN file and save output.")
    parser.add_argument("input_file", help="Path to the input ALN file")
    parser.add_argument("output_file", help="Path to the output PDB file")

    args = parser.parse_args()

    run_dmpfold(args.input_file, args.output_file)
