### combining all features and ranking them

### Here is saved command prompts to make it easier to create snakemake
# python workflow/scripts/apply_function.py results/hydrophobicity_results.csv results/pI_results.csv results/molecular_weight.csv results/tm_scores/tm_score_gen_seq.csv results/stability.csv results/affinity.csv results/specificity.csv --output_file results/final_results.csv
# python workflow/scripts/weighted_sum.py results/final_results.csv results/weighted_results.csv --a 1.2 --b 0.8 --c 0.001 --d 0.001 --e 2.0 --f 6.5 --g 6.7 --h 4.5

# defining input 
hydrophobicity = "results/hydrophobicity_results.csv"
pI = "results/pI_results.csv"
weight_length = "results/molecular_weight.csv"
stability = "results/stability.csv"
affinity = "results/affinity.csv"
specificity = "results/specificity.csv
final = "results/final_results.csv"
score = "results/weighted_results.csv"

rule all:
    input:
        hydrophobicity,
        pI,
        weight_length,
        stability,
        affinity,
        specificity,
        final,
        score

rule combine_sequences:
    input: hydrophobicity, pI, weight_length, stability, affinity, specificity
    output: final
    shell: "python workflow/scripts/apply_function.py {input[0]} {input[1]} {input[2]} {input[3]} {input[4]} {input[5]} --output_file final"

# Here change numbers next to a,b,c,d to get wanted results
rule score_sequences:
    input: final
    output: score
    shell: "python workflow/scripts/weighted_sum.py {input} {output} --a 1.2 --b 0.8 --c 0.001 --d 0.001 --e 2.0 --f 6.5 --g 6.7 --h 4.5"