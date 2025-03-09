#include: "workflow/rules/sofia.smk"

FASTA_FILE = "z1_resources/gen+nat.fasta"
PI_CSV = "results/pI_results.csv"

rule all:
    input:
        "results/pI_results.csv",
        


rule compute_pI:
    input:
        FASTA_FILE
    output:
        PI_CSV
    shell:
        "set -e; echo 'Starting compute_pI'; python workflow/scripts/pI.py -i {input} -o {output}; echo 'Finished compute_pI'"



