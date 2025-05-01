import glob
import os

# Define the path to the MGLTools script (edit this if the path changes)
prepare_receptor_script = "workflow/scripts/prepare_receptor4.py"

# Extract all base names from 'nat' PDBs
nat_pdb_files = glob.glob("results/nat/renamed_files/*.pdb")
names_nat = [os.path.splitext(os.path.basename(f))[0] for f in nat_pdb_files]

# Extract all base names from 'gen' PDBs
gen_pdb_files = glob.glob("results/gen/*.pdb")
names_gen = [os.path.splitext(os.path.basename(f))[0] for f in gen_pdb_files]

rule all:
    input:
        expand("results/converted_pdbqt_natural/{name}.pdbqt", name=names_nat),
        expand("results/converted_pdbqt/{name}.pdbqt", name=names_gen),
        "results/docking/co2.pdbqt",
        expand("results/docking/docked_{name}.pdbqt", name=names_gen),
        expand("results/docking/minimized_{name}.pdbqt", name=names_gen),
        expand("results/docking/docking_results_{name}.txt", name=names_gen)

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
        "results/nat/renamed_files/{name}.pdb"
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