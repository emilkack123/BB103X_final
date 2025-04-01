### Define file paths ###

MOLECULAR_WEIGHT_CSV = "results/molecular_weight.csv"
MOLECULAR_WEIGHT_BOXPLOT = "results/molecular_weight_boxplot.png"
MOLECULAR_WEIGHT_HISTOGRAM = "results/molecular_weight_histogram.png"
SEQUENCE_LENGTH_BOXPLOT = "results/sequence_length_boxplot.png"
SCATTER_PLOT = "results/scatterplot.png"

DISTANCE_MATRIX = "results/distmat.tsv"
HEATMAP_PLOT = "results/heatmap.png"

### Rule to compute molecular weight and sequence length ###
rule compute_molecular_weight:
    input:
        gen="resources/rubisco_sequences/gen.fa",
        nat="resources/rubisco_sequences/nat.fa"
    output:
        MOLECULAR_WEIGHT_CSV
    shell:
        "python workflow/scripts/compute_molecular_weight.py {input.gen} {input.nat} {output}"

### Rule to generate molecular weight & sequence length plots ###
rule plot_molecular_weight_length:
    input:
        MOLECULAR_WEIGHT_CSV
    output:
        MOLECULAR_WEIGHT_BOXPLOT,
        MOLECULAR_WEIGHT_HISTOGRAM,
        SEQUENCE_LENGTH_BOXPLOT,
        SCATTER_PLOT
    shell:
        "mkdir -p results/ && python workflow/scripts/plot_molecular_weight_length.py {input} results/molecular_weight_analysis"

### Rule to compute distance matrix ###
rule compute_distance_matrix:
    input:
        gen="resources/rubisco_sequences/gen.fa",
        nat="resources/rubisco_sequences/nat.fa"
    output:
        DISTANCE_MATRIX
    shell:
        "python workflow/scripts/compute_distance_matrix.py {input.gen} {input.nat} {output}"

### Rule to plot heatmap from distance matrix ###
rule plot_heatmap:
    input:
        DISTANCE_MATRIX
    output:
        HEATMAP_PLOT
    shell:
        "python workflow/scripts/plot_heatmap.py {input} {output}"

### Final rule to run everything ###
rule all:
    input:
        MOLECULAR_WEIGHT_CSV,
        MOLECULAR_WEIGHT_BOXPLOT,
        MOLECULAR_WEIGHT_HISTOGRAM,
        SEQUENCE_LENGTH_BOXPLOT,
        SCATTER_PLOT,
        DISTANCE_MATRIX,
        HEATMAP_PLOT
