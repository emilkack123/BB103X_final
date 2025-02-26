FASTA_FILE = "resources/dragon_radii_updated.fasta"
PI_CSV = "results/pI_results.csv"
HYDROPHOBICITY_CSV = "results/hydrophobicity_results.csv"

rule all:
input: PI_CSV


rule compute_pI:
    input:
        FASTA_FILE
    output:
        PI_CSV
    shell:
        "python workflow/scripts/pI.py -i {input} -o {output}"

rule compute_hydrophobicity:
    input:
        FASTA_FILE
    output:
        HYDROPHOBICITY_CSV
    shell:
        "python workflow/scripts/hydrophobicity.py -i {input} -o {output}"

