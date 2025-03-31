##############################################################################
# Final target: Use the OmegaFold output directory as the final product
##############################################################################
rule all:
    input:
        lambda wildcards: f"results/{config['seq']}"

##############################################################################
# Structure prediction rule
##############################################################################
checkpoint run_omegafold:
    input:
        "resources/rubisco_sequences/{seq}.fa"
    output:
        directory("results/{seq}")
    conda:
        "workflow/envs/omegafold.yaml"
    shell:
        """
        # Run OmegaFold with the input FASTA and output subdirectory.
        omegafold {input[0]} {output}
        """
#Call by: snakemake --use-conda --conda-frontend conda --cores 1 --config seq=gen
