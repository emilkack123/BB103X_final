import re
import glob
import os

# Define the path to the MGLTools script (edit this if the path changes)
prepare_receptor_script = "workflow/scripts/prepare_receptor4.py"

# Extract all base names from 'nat' PDBs
nat_pdb_files = glob.glob("results/nat_renamed/*.pdb")
names_nat = [os.path.splitext(os.path.basename(f))[0] for f in nat_pdb_files]

# Extract all base names from 'gen' PDBs
gen_pdb_files = glob.glob("results/gen/*.pdb")
names_gen = [os.path.splitext(os.path.basename(f))[0] for f in gen_pdb_files]


# Define the paths for the input and output files
input_fasta_1 = "resources/rubisco_sequences/dragon_radii_updated.fasta"
input_fasta_2 = "resources/rubisco_sequences/NaturalRubisco.fasta"
pca_output_plot = "results/PCA_and_K-mean/pca_plot.png"
kmeans_output_plot = "results/PCA_and_K-mean/kmeans_plot_pca_with_clusters.png"
pca_output_scree = "results/PCA_and_K-mean/pca_plot_scree.png"

hydrophobicity = "results/hydrophobicity_results.csv"
pI = "results/pI_results.csv"
weight_length = "results/molecular_weight.csv"
stability = "results/confidence_scores.csv"
final = "results/final_characteristics.csv"
score = "results/weighted_results.csv"

# Path to the new K-means and PCA script
kmeans_script = "workflow/scripts/k-mean.py"

# Hydrophobicity and PI
FASTA_FILE = "results/gen+NaturalRubisco.fastasta"
PI_CSV = "results/pI_results.csv"
HYDROPHOBICITY_CSV = "results/hydrophobicity_results.csv"

SAMPLES = ["results/gen/*.pdb"]  # All generated PDB files 

# Define input and output files for t-sne plot
gen_seqs = "resources/rubisco_sequences/dragon_radii_updated.fasta"
nat_seqs = "resources/rubisco_sequences/NaturalRubisco.fasta"
all_seqs = "results/rubisco.fasta"
cleaned_seqs = "results/rubisco_cleaned.fasta"
filtering_log = "results/rubisco_filtering.log"
msa = "results/rubisco_msa.fasta" 
dist_mat = "results/rubisco_dist_mat.tsv"
output_csv = "results/rubisco.csv"
csv_wNewCol = "results/rubisco_updated.csv"
csv_final = "results/rubisco_final.csv"
cluster_plot = "results/rubisco_clusters.png"
length = "results/length_histogram.png"

# Molecular weight plots
MOLECULAR_WEIGHT_CSV = "results/molecular_weight_results.csv"
MOLECULAR_WEIGHT_BOXPLOT = "results/molecular_weight_boxplot.png"
MOLECULAR_WEIGHT_HISTOGRAM = "results/molecular_weight_histogram.png"
SEQUENCE_LENGTH_BOXPLOT = "results/sequence_length_boxplot.png"
SCATTER_PLOT = "results/scatterplot.png"

# Distance Matrix + Heatmap
DISTANCE_MATRIX = "results/distmat.tsv"
HEATMAP_PLOT = "results/heatmap.png"

#Iupred
iupred_raw_output ="results/iupred_output.txt"
disorder_metrics_csv = "results/disorder_metrics.csv"

# Define the input and output directories
input_dir = 'results/gen/'
output_dir = 'results/converted_pdbqt/'

# Ensure the output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Get list of PDB filenames without extension from results/gen/
gen_pdb_names = [f[:-4] for f in os.listdir("results/gen") if f.endswith(".pdb")]

# Rule to generate final outputs (PCA, K-means, TM-score results, and confidence scores)
rule all:
    input:
        pca_output_plot,
        pca_output_scree,           
        kmeans_output_plot,        
        "results/boxplot.png",
        "results/hydrophobicity_boxplot.png",
        nat_seqs,
        all_seqs,
        cleaned_seqs,
        filtering_log,
        output_csv,
        length,
        msa,
        dist_mat,
        cluster_plot,
        hydrophobicity,
        pI,       
        stability,
        DISTANCE_MATRIX,
        HEATMAP_PLOT,
        "results/nat_renamed/renamed_files_log.csv",
        expand("results/converted_pdbqt_natural/{name}.pdbqt", name=names_nat),
        expand("results/converted_pdbqt/{name}.pdbqt", name=names_gen),
        "results/docking/co2.pdbqt",
        expand("results/docking/docked_{name}.pdbqt", name=names_gen),
        expand("results/docking/minimized_{name}.pdbqt", name=names_gen),
        expand("results/docking/docking_results_{name}.txt", name=names_gen),
        "results/confidence_scores.csv",
        "results/tm_scores/tm-scores.csv",
        "results/ranked_sequences.csv",
        iupred_raw_output,
        disorder_metrics_csv,
        final,
        score,
        "results/gen",  
        "results/nat",
        "results/docking/co2.pdbqt",
        expand("results/docking/docking_results_{name}.txt", name=gen_pdb_names)

        
# Rule to run the PCA script
rule run_pca:
    input:
        input_fasta_1,
        input_fasta_2
    output:
        pca_output_plot,
        pca_output_scree
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/PCA.py {input[0]} {input[1]} {output[0]}"

# Rule to run the K-means clustering and PCA visualization script
rule run_kmeans_pca:
    input:
        input_fasta_1,
        input_fasta_2
    output:
        kmeans_output_plot
    conda:
        "workflow/envs/environment.yml"
    params:
        script=kmeans_script
    shell:
        "python {params.script} '{input[0]}' '{input[1]}' {output}"

rule concat_rubisco:
    input:
        "resources/rubisco_sequences/dragon_radii_updated.fasta",
        "resources/rubisco_sequences/NaturalRubisco.fasta"
    output:
        "results/gen+NaturalRubisco.fastasta"
    conda:
        "workflow/envs/environment.yml"
    shell:
        "cat {input} > {output}"
        
rule compute_pI:
    input:
        gen_fasta="resources/rubisco_sequences/dragon_radii_updated.fasta",
        nat_fasta="resources/rubisco_sequences/NaturalRubisco.fasta"
    output:
        csv="results/pI_results.csv"
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/pI.py {input.gen_fasta} {input.nat_fasta} {output.csv}"

rule compute_hydrophobicity:
    input:
        gen_fasta="resources/rubisco_sequences/dragon_radii_updated.fasta",
        nat_fasta="resources/rubisco_sequences/NaturalRubisco.fasta"
    output:
        "results/hydrophobicity_results.csv"
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/hydrophobicity.py {input.gen_fasta} {input.nat_fasta} {output}"


rule pI_boxplot:
    input:
        csv="results/pI_results.csv"
    output:
        png="results/pI_boxplot.png"
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/boxplot_pI.py --csv {input.csv} --output {output.png}"

rule hydrophobicity_boxplot:
    input:
        csv="results/hydrophobicity_results.csv"
    output:
        png="results/hydrophobicity_boxplot.png"
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/boxplot_hydrophobicity.py --csv {input.csv} --output {output.png}"

rule combine_sequences:
    input: gen_seqs, nat_seqs
    output: all_seqs
    conda:
        "workflow/envs/environment.yml"
    shell: "cat {input} > {output}"

rule rename_nat_files:
    input:
        folder="results/nat"
    output:
        log="results/nat_renamed/renamed_files_log.csv"
    conda:
        "workflow/envs/environment.yml"
    shell:
        """
        python workflow/scripts/rename_nat.py {input.folder} {output.log}
        """

rule clean_fasta:
    input: all_seqs
    output: cleaned_seqs
    conda:
        "workflow/envs/environment.yml"
    log: filtering_log
    shell: "workflow/scripts/clean_fasta.py --to-uppercase {input} {output} > {log}"

rule fasta_to_csv:
    input: cleaned_seqs
    output: output_csv  # FIXED: Ensuring this is unique
    conda:
        "workflow/envs/environment.yml"
    shell: "workflow/scripts/fasta_to_csv.py {input} {output}"

rule add_origin_column:
    input: output_csv
    output: csv_wNewCol  # modifies in place
    conda:
        "workflow/envs/environment.yml"
    shell: "workflow/scripts/add_origin_column.py {input} {output}"

rule length_histogram:
    input: csv_wNewCol
    output: length

    conda:
        "workflow/envs/environment.yml"

    shell: "python workflow/scripts/sequence_histogram.py {input} {output}"

rule multiple_sequence_alignment:
    input: cleaned_seqs
    output: msa, dist_mat
    conda:
        "workflow/envs/environment.yml"
    shell: "clustalo -i {input} -o {output[0]} --distmat-out={output[1]} --full"

rule add_closest_column:
    input: dist_mat, csv_wNewCol
    output: csv_final  # modifies in place
    conda:
        "workflow/envs/environment.yml"
    shell: "workflow/scripts/add_closest_column.py {input[0]} {input[1]} {output} --sort"

rule plot_clustering:
    input: dist_mat, csv_final
    output: cluster_plot
    conda:
        "workflow/envs/environment.yml"
    shell: "python workflow/scripts/plot_clustering.py {input[0]} {output} --metadata {input[1]}"

rule compute_molecular_weight:
    input:
        gen_fasta="resources/rubisco_sequences/dragon_radii_updated.fasta",
        nat_fasta="resources/rubisco_sequences/NaturalRubisco.fasta"
    output:
        csv="results/molecular_weight_results.csv"
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/compute_molecular_weight.py {input.gen_fasta} {input.nat_fasta} {output.csv}"

rule plot_molecular_weight_length:
    input: MOLECULAR_WEIGHT_CSV
    output:
        MOLECULAR_WEIGHT_BOXPLOT,
        MOLECULAR_WEIGHT_HISTOGRAM,
        SEQUENCE_LENGTH_BOXPLOT,
        SCATTER_PLOT
    conda:
        "workflow/envs/environment.yml"
    shell: "mkdir -p results/ && python workflow/scripts/plot_molecular_weight_length.py {input} results/molecular_weight_analysis"

rule compute_distance_matrix:
    input: gen=input_fasta_1, nat=input_fasta_2
    output: DISTANCE_MATRIX
    conda:
        "workflow/envs/environment.yml"
    shell: "python workflow/scripts/compute_distance_matrix.py {input.gen} {input.nat} {output}"

rule plot_heatmap:
    input:
        matrix="results/distmat.tsv"
    output:
        heatmap="results/heatmap.png"
    conda:
        "workflow/envs/environment.yml"
    shell:
        """
        mkdir -p results
        python workflow/scripts/plot_heatmap.py {input.matrix} {output.heatmap}
        """
rule dendrogram:
    input:
        matrix="results/distmat.tsv"
    output:
        plot="results/dendrogram.png"
    conda:
        "workflow/envs/environment.yml"
    shell:
        """
        mkdir -p results
        python workflow/scripts/dendrogram.py {input.matrix} {output.plot}
        """

# Add a rule to convert PDB to PDBQT using the Python script
rule convert_pdb_to_pdbqt_gen:
    input:
        pdb="results/gen/{name}.pdb"
    output:
        pdbqt="results/converted_pdbqt/{name}.pdbqt"
    shell:
        """
        source activate autodock_py2.yml && \
        python2 {prepare_receptor_script} \
        -r {input.pdb} -o {output.pdbqt}
        """

rule convert_pdb_to_pdbqt_nat:
    input:
        "results/nat_renamed/{name}.pdb"
    output:
        pdbqt="results/converted_pdbqt_natural/{name}.pdbqt"
    shell:
        """
        source activate autodock_py2.yml && \
        python2 {prepare_receptor_script} \
        -r {input} -o {output.pdbqt}
        """

rule docking:
    input:
        receptor_file="results/converted_pdbqt/{name}.pdbqt",
        ligand_file="results/docking/co2.pdbqt"
    output:
        docked="results/docking/docked_{name}.pdbqt",
        minimized="results/docking/minimized_{name}.pdbqt",
        result="results/docking/docking_results_{name}.txt"
    conda:
        "workflow/envs/vina_env.yml"
    params:
        script="workflow/scripts/docking_of_Rubisco.py"
    shell:
        """
        python {params.script} --receptor_file {input.receptor_file} \
                                --ligand_file {input.ligand_file} \
                                --docked_output {output.docked} \
                                --minimized_output {output.minimized} \
                                --result_output {output.result}
        """

rule compute_confidence_scores:
    input:
        gen_folder="results/gen",
        nat_folder="results/nat"
    output:
        confidence_scores="results/confidence_scores.csv"
    conda:
        "workflow/envs/environment.yml"
    params:
        script="workflow/scripts/compute_confidence_score.py"
    shell:
        """
        python {params.script} \
            --folders {input.gen_folder} {input.nat_folder} \
            --output {output.confidence_scores}
        """

rule tm_score:
    input:
        confidence_scores="results/confidence_scores.csv",
        gen_folder="results/gen",
        nat_folder="results/nat"
    output:
        tm_scores="results/tm_scores/tm-scores.csv"
    conda:
        "workflow/envs/environment.yml"
    params:
        script="workflow/scripts/TM-score.py"
    shell:
        """
        python {params.script} \
            --confidence_scores {input.confidence_scores} \
            --gen_folder {input.gen_folder} \
            --nat_folder {input.nat_folder} \
            --output {output.tm_scores}
        """

# Rule to combine results from various data sources into a final CSV

rule run_iupred2a:
    input:
        fasta=input_fasta_1
    output:
        txt=iupred_raw_output
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python external_tools/iupred2a/iupred2a.py {input.fasta} long > {output.txt}"

rule parse_disorder:
    input:
        fasta=input_fasta_1,
        txt=iupred_raw_output
    output:
        csv=disorder_metrics_csv
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/parse_disorder_by_length.py {input.fasta} {input.txt} {output.csv}"

        
rule plot_disorder_metrics:
    input:
        csv=disorder_metrics_csv
    output:
        dir="results/disorder_plots/hist_percent_disorder.png"
    conda:
        "workflow/envs/environment.yml"
    params:
        outdir="results/disorder_plots"
    shell:
        "python workflow/scripts/plot_disorder_metrics.py {input.csv} --output_dir {params.outdir}"

rule combine_sequences_2:
    input:
        hydro="results/hydrophobicity_results.csv",
        pi="results/pI_results.csv",
        mol_weight="results/molecular_weight.csv",
        tm_score="results/tm_scores/tm-scores.csv",
        stability="results/confidence_scores.csv",
        disorder="results/disorder_metrics.csv",
        docking_folder="results/docking"
    output:
        "results/final_characteristics.csv"
    conda:
        "workflow/envs/environment.yml"
    shell:
        """
        python workflow/scripts/combined_final_results.py {input.hydro} {input.pi} {input.mol_weight} {input.tm_score} {input.stability} {input.disorder} {input.docking_folder} --output_file {output}
        """
# Here change numbers next to a,b,c,d to get wanted results
rule score_sequences:
    input: final
    output: score
    conda:
        "workflow/envs/environment.yml"
    shell: "python workflow/scripts/weighted_sum.py {input} {output} --a -1.2 --b -0.8 --c -0.001 --d -0.001 --e 2.0 --f 6.5 --g 2 --h 2 --j 10"

rule rank_sequences:
    input:
        "results/weighted_results.csv"  # Input weighted results file
    output:
        "results/ranked_sequences.csv"  # Output ranked sequences file
    conda:
        "workflow/envs/environment.yml"
    shell:
        "python workflow/scripts/ranking_sequences.py {input} {output}"

checkpoint run_omegafold:
    wildcard_constraints:
        seq="[^.]+"
    input:
        "resources/rubisco_sequences/{seq}.fa"
    output:
        directory("results/{seq}")
    conda:
        "workflow/envs/omegafold.yaml"
    shell:
        """
        omegafold {input} {output}
        """

