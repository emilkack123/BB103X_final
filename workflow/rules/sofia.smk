FASTA_FILE = "resources/dragon_radii_updated.fasta"
PI_CSV = "results/pI_results.csv"
HYDROPHOBICITY_CSV = "results/hydrophobicity_results.csv"

rule all:
    input:
        "results/pI_results.csv",
        "results/hydrophobicity_results.csv"


rule compute_pI:
    input:
        FASTA_FILE
    output:
        PI_CSV
    shell:
        "set -e; echo 'Starting compute_pI'; python workflow/scripts/pI.py -i {input} -o {output}; echo 'Finished compute_pI'"



rule compute_hydrophobicity:
    input:
        FASTA_FILE
    output:
        HYDROPHOBICITY_CSV
    shell:
        "python workflow/scripts/hydrophobicity.py -i {input} -o {output}"

