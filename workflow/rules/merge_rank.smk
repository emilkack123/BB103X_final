### combining all features and ranking them

### Here is saved command prompts to make it easier to create snakemake
# python workflow/scripts/apply_function.py results/hydrophobicity_results.csv results/pI_results.csv results/molecular_weight.csv results/tm_scores/tm-scores.csv results/confidence_scores.csv --output_file results/final_results.csv
# python workflow/scripts/weighted_sum.py results/final_results.csv results/weighted_results.csv --a -1.2 --b -0.8 --c -0.001 --d -0.001 --e 2.0 --f 6.5
# defining input 
hydrophobicity = "results/hydrophobicity_results.csv"
pI = "results/pI_results.csv"
weight_length = "results/molecular_weight.csv"
stability = "results/confidence_scores.csv"
final = "results/final_results.csv"
score = "results/weighted_results.csv"

rule all:
    input:
        hydrophobicity,
        pI,
        weight_length,
        stability,
        final,
        score

rule combine_sequences:
    input:
        hydro="results/hydrophobicity_results.csv",
        pi="results/pI_results.csv",
        mol_weight="results/molecular_weight.csv",
        tm_score="results/tm_scores/tm_score_gen_seq.csv",
        stability="results/stability.csv"
    output:
        "results/final_results.csv"
    shell:
        """
        python workflow/scripts/apply_function.py {input.hydro} {input.pi} {input.mol_weight} {input.tm_score} {input.stability} --output_file {output}
        """
# Here change numbers next to a,b,c,d to get wanted results
rule score_sequences:
    input: final
    output: score
    shell: "python workflow/scripts/weighted_sum.py {input} {output} --a -1.2 --b -0.8 --c -0.001 --d -0.001 --e 2.0 --f 6.5"