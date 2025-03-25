SAMPLES = ["nat", "gen"]
SEQS = range(1, 11)  # Antal sekvenser i varje aln-fil

rule all:
    input:
        expand("results/{sample}_models/model_{sample}_seq{seq}.pdb", sample=SAMPLES, seq=SEQS)

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

rule split_aln:
    input:
        "results/{sample}_aln_file.aln"
    output:
        "results/{sample}_targets/seq{seq}.aln"
    shell:
        """
        mkdir -p results/{wildcards.sample}_targets
        awk '{{print $0 > "results/{wildcards.sample}_targets/seq" NR ".aln"}}' {input}
        """

rule run_dmpfold_per_seq:
    input:
        "results/{sample}_targets/seq{seq}.aln"
    output:
        "results/{sample}_models/model_{sample}_seq{seq}.pdb"
    shell:
        """
        mkdir -p results/{wildcards.sample}_models
        echo "🚀 Running dmpfold for {wildcards.sample}, sequence {wildcards.seq}..."
        python workflow/scripts/run_dmpfold2.py {input} {output}
        """
