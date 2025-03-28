### combining hydrophobicity and pI not final
# python workflow/scripts/apply_function.py results/hydrophobicity_results.csv results/pI_results.csv results/molecular_weight.csv results/tm_scores/tm_score_gen_seq.csv --output_file results/final_results.csv
# python workflow/scripts/weighted_sum.py results/final_results.csv results/weighted_results.csv --a 1.2 --b 0.8 --c 0.001 --d 0.001 --e 2.0

# defining input 
hydrophobicity = "results/hydrophobicity_results.csv"
pI = "results/pI_results.csv"
weight_length = "results/molecular_weight.csv"
tm_score = "results/tm_score/tm_score_gen_seq.csv"
final = "results/final_results.csv"
score = "results/weighted_results.csv"

rule all:
    input:
        hydrophobicity,
        pI,
        weight_length,
        tm_score,
        final,
        score

rule combine_sequences:
    input: hydrophobicity, pI, weight_length, tm_score
    output: final
    shell: "python workflow/scripts/apply_function.py {input[0]} {input[1]} {input[2]} {input[3]} --output_file final"

# Here change numbers next to a,b,c,d to get wanted results
rule score_sequences:
    input: final
    output: score
    shell: "python workflow/scripts/weighted_sum.py {input} {output} --a 1.2 --b 0.8 --c 0.001 --d 0.001 --e 2.00"
