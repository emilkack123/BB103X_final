rule predict_structures_ahmad:
    input:
        "resources/cleaned.fasta"
    output:
        expand("results/structures/{seq}.pdb", seq=[rec.id for rec in SeqIO.parse("resources/cleaned.fasta", "fasta")])
    script:
        "workflow/scripts/predict_structures.py"

rule compare_structures_ahmad:
    input:
        expand("results/structures/{seq}.pdb", seq=[rec.id for rec in SeqIO.parse("resources/cleaned.fasta", "fasta")])
    output:
        "results/comparisons/rmsd_results_ahmad.txt"
    script:
        "workflow/scripts/compare_structures.py"


rule clone_external_tool:
    output:
        "workflow/external_tool_installed.txt"
    shell:
        """
        git clone https://github.com/example/external-tool.git workflow/external_tool
        touch workflow/external_tool_installed.txt
        """

rule normalize_data:
    input:
        "results/comparisons/rmsd_results_ahmad.txt"
    output:
        "results/normalized_data_ahmad.txt"
    script:
        "workflow/scripts/normalize_data.py"
