### combining hydrophobicity and pI not final
# python workflow/scripts/apply_function.py results/hydrophobicity_results.csv results/pI_results.csv results/molecular_weight.csv --output_file results/final_results.csv

# defining input 
hydrophobicity = "results/hydrophobicity_results.csv"
pI = "results/pI_results.csv"
weight_length = "results/molecular_weight.csv"
final = "results/final_results.csv"

rule all:
    input:
        hydrophobicity,
        pI,
        weight_length,
        final

rule combine_sequences:
    input: hydrophobicity, pI, weight_length
    output: final
    shell: "python workflow/scripts/apply_function.py {input[0]} {input[1]} {input[1]} --output_file final"