### combining hydrophobicity and pI not final
# python workflow/scripts/apply_function.py results/hydrophobicity_results.csv results/pI_results.csv results/molecular_weight.csv --output_file results/final_results.csv
# python workflow/scripts/weighted_sum.py results/final_results.csv results/weighted_results.csv --a 1.2 --b 0.8 --c 0.001 --d 0.001

# defining input 
hydrophobicity = "results/hydrophobicity_results.csv"
pI = "results/pI_results.csv"
weight_length = "results/molecular_weight.csv"
final = "results/final_results.csv"
score = "results/weighted_results.csv"

rule all:
    input:
        hydrophobicity,
        pI,
        weight_length,
        final,
        score

rule combine_sequences:
    input: hydrophobicity, pI, weight_length
    output: final
    shell: "python workflow/scripts/apply_function.py {input[0]} {input[1]} {input[1]} --output_file final"

# Here change numbers next to a,b,c,d to get wanted results
rule score_sequences:
    input: final
    output: score
    shell: "python workflow/scripts/weighted_sum.py {input} {output} --a 1.2 --b 0.8 --c 0.001 --d 0.001"
