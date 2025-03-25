
rule all:
    input:
        "results/boxplot.png","results/hydrophobicity_boxplot.png"
        

rule concat_rubisco:
    input:
        "resources/rubisco_sequences/gen.fa",
        "resources/rubisco_sequences/nat.fa"
    output:
        "results/gen+nat.fasta"
    shell:
        "cat {input} > {output}"

rule compute_pI:
    input:
        "results/gen+nat.fasta"
    output:
        "results/pI_results.csv"
    shell:
        "set -e; echo 'Starting compute_pI'; python workflow/scripts/pI.py -i {input} -o {output}; echo 'Finished compute_pI'"



rule compute_hydrophobicity:
    input:
        "results/gen+nat.fasta"
    output:
        "results/hydrophobicity_results.csv"
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
