rule all:
    input:
        "merged_metrics.csv"

rule merge_metrics:
    input:
        pI="results/pI_results.csv",
        hydrophobicity="results/hydrophobicity_results.csv",
        tm_score="results/tm_scores/tm_score_results.csv",
        molecular_weight="results/molecular_weight.csv"
    output:
        "merged_metrics.csv"
    shell:
        """
        python workflow/scripts/apply_function.py \
            --files {input.pI} {input.hydrophobicity} {input.tm_score} {input.molecular_weight} \
            --keys "ID" "ID" "PDB File" "Sequence_ID" \
            --data_cols pI Hydrophobicity TM-score "Sequence_Length,Molecular_Weight" \
            --metrics pI_results hydrophobicity_results tm_score_results "Sequence_Length,Molecular_Weight" \
            --output {output}
        """
