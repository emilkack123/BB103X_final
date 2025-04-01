# Define input and output files
gen_seqs = "resources/rubisco_sequences/gen.fa"
nat_seqs = "resources/rubisco_sequences/nat.fa"
all_seqs = "results/rubisco.fasta"
cleaned_seqs = "results/rubisco_cleaned.fasta"
filtering_log = "results/rubisco_filtering.log"
msa = "results/rubisco_msa.fasta" 
dist_mat = "results/rubisco_dist_mat.tsv"
output_csv = "results/rubisco.csv"
csv_wNewCol = "results/rubisco_updated.csv"
csv_final = "results/rubisco_final.csv"
cluster_plot = "results/rubisco_clusters.png"

# Rule to generate final outputs (PCA, K-means, TM-score results, and confidence scores)
rule all:
    input:
        nat_seqs,
        all_seqs,
        cleaned_seqs,
        filtering_log,
        output_csv,
        msa,
        dist_mat,
        cluster_plot

rule combine_sequences:
    input: gen_seqs, nat_seqs
    output: all_seqs
    shell: "cat {input} > {output}"

rule clean_fasta:
    input: all_seqs
    output: cleaned_seqs
    log: filtering_log
    shell: "workflow/scripts/clean_fasta.py --to-uppercase {input} {output} > {log}"

rule fasta_to_csv:
    input: cleaned_seqs
    output: output_csv  # FIXED: Ensuring this is unique
    shell: "workflow/scripts/fasta_to_csv.py {input} {output}"

rule add_origin_column:
    input: output_csv
    output: csv_wNewCol  # modifies in place
    shell: "workflow/scripts/add_origin_column.py {input} {output}"

rule multiple_sequence_alignment:
    input: cleaned_seqs
    output: msa, dist_mat
    shell: "clustalo -i {input} -o {output[0]} --distmat-out={output[1]} --full"

rule add_closest_column:
    input: dist_mat, csv_wNewCol
    output: csv_final  # modifies in place
    shell: "workflow/scripts/add_closest_column.py {input[0]} {input[1]} {output} --sort"

rule plot_clustering:
    input: dist_mat, csv_final
    output: cluster_plot
    shell: "python workflow/scripts/plot_clustering.py {input[0]} {output} --metadata {input[1]}"