SAMPLES = ["nat", "gen"]

# Dictionaries med målmappar beroende på sample
TARGET_DIRS = {
    "nat": "results/z4_targets_natural",
    "gen": "results/z2_targets_gen"
}
MODEL_DIRS = {
    "nat": "results/z5_models_natural",
    "gen": "results/z3_models_gen"
}

rule all:
    input:
        expand("results/{sample}_model_1.pdb", sample=SAMPLES)

rule convert_fasta_upper:
    input:
        "resources/rubisco_sequences/{sample}.fa"
    output:
        "results/{sample}_upper.fa"
    shell:
        "mkdir -p results && python workflow/scripts/convert_fasta_upper.py {input} {output}"

rule fasta_to_aln:
    input:
        "results/{sample}_upper.fa"
    output:
        "results/{sample}_aln_file.aln"
    shell:
        "python workflow/scripts/fasta_to_aln.py {input} {output}"

rule run_dmpfold:
    input:
        "results/{sample}_aln_file.aln"
    # Output: En fil med namnet results/{sample}_model_1.pdb (vi kommer senare flytta dit filen som dmpfold skapar)
    output:
        "results/{sample}_model_1.pdb"
    params:
        target_dir = lambda wc: TARGET_DIRS[wc.sample],
        model_dir  = lambda wc: MODEL_DIRS[wc.sample]
    conda:
        "workflow/envs/bioenv.yml"
    shell:
        "mkdir -p {params.target_dir} {params.model_dir} && "
        "python workflow/scripts/run_dmpfold2.py {input} --target_dir {params.target_dir} --model_dir {params.model_dir} && "
        "mv {params.model_dir}/model_1.pdb {output}"
