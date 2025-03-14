FASTA_FILE = "resources/gen+nat.fasta"
PI_CSV = "results/pI_results.csv"
HYDROPHOBICITY_CSV = "results/hydrophobicity_results.csv"

rule all:
    input:
        "results/boxplot.png","results/hydrophobicity_boxplot.png"
        


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

rule boxplot_pI:
    input:
        csv="results/pI_results.csv"
    output:
        png="results/boxplot.png"
    shell:
        "python workflow/scripts/boxplot_pI.py --csv {input.csv} --output {output.png}"

rule hydrophobicity_boxplot:
    input:
        csv="results/hydrophobicity_results.csv"
    output:
        png="results/hydrophobicity_boxplot.png"
    shell:
        "python workflow/scripts/boxplot_hydrophobicity.py --csv {input.csv} --output {output.png}"
