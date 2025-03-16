rule all:
    input:
        "z3_models_gen/model_1.pdb"

rule convert_fasta_upper:
    input:
        "resources/rubisco_sequences/gen.fa"
    output:
        "results/gen_upper.fa"
    shell:
        "python workflow/scripts/convert_fasta_upper.py {input} {output}"

rule fasta_to_aln:
    input:
        "results/gen_upper.fa"
    output:
        "results/gen_aln_file.aln"
    shell:
        "python workflow/scripts/fasta_to_aln.py {input} {output}"

rule run_dmpfold:
    input:
        "results/gen_aln_file.aln"
    output:
        "results/z3_models_gen/model_1.pdb"
    shell:
        "python workflow/scripts/run_dmpfold2.py {input} --target_dir results/z2_targets_gen --model_dir results/z3_models_gen"
