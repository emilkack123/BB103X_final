rule all:
    input:
        "results/z5_models_natural/model_1.pdb"

# Pipeline för naturliga sekvenser (nat)
rule convert_fasta_upper_nat:
    input:
        "resources/rubisco_sequences/nat.fa"
    output:
        "results/nat_upper.fa"
    shell:
        "mkdir -p results && python workflow/scripts/convert_fasta_upper.py {input} {output}"

rule fasta_to_aln_nat:
    input:
        "results/nat_upper.fa"
    output:
        "results/nat_aln_file.aln"
    shell:
        "python workflow/scripts/fasta_to_aln.py {input} {output}"

rule run_dmpfold_nat:
    input:
        "results/nat_aln_file.aln"
    output:
        "results/z5_models_natural/model_1.pdb"
    conda:
        "workflow/envs/bioenv.yml"
    shell:
        "mkdir -p results/z4_targets_natural results/z5_models_natural && "
        "python workflow/scripts/run_dmpfold2.py {input} --target_dir results/z4_targets_natural --model_dir results/z5_models_natural"
