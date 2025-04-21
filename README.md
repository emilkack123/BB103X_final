# BB103X_final: Computational Pipeline for Rubisco Sequence Evaluation
## Overview
This project is part of the BB103X bachelor's thesis at KTH, aimed at developing a computational pipeline for evaluating AI-generated Rubisco amino acid sequences. Rubisco, the key enzyme for carbon fixation, is notoriously inefficient in its natural form. By analyzing both generated and natural sequences, this pipeline enables high-throughput screening to identify potentially improved Rubisco variants for wet-lab experiments.

The pipeline is designed using Snakemake and built for modular, reproducible, and scalable protein engineering workflows.


## Pipeline structure
```bash
BB103X_final/
│
├── .snakemake/           

├── config/               

├── resources/            

├── results/              

├── workflow/

│   ├── rules/            

│   ├── scripts/          

│   ├── envs/             
│       ├── environment.yml       
│       ├── bioenv.yml            
│       ├── omegafold.yaml        
│       ├── snakemake_env.yaml    
│       └── t-SNE_env.yml   
├── Snakefile                           
├── LICENSE
├── README.md
└── .gitignore
```

## Pipeline fuctionalities
![Pipeline DAG](dag.png)


1) Preprocessing

- Combine, clean, and convert FASTA sequences.

2) Sequence Analysis

- Compute pI, hydrophobicity, molecular weight, and sequence length.

3) Perform multiple sequence alignment with Clustal Omega.

- Structural Evaluation

4) Predict 3D structures with OmegaFold.

- Calculate TM-scores.

5) Predict Affinity with 3D structures

- Calculate affinity 

6) Calculate number of disorder sequences and percent disorder

6) Visualization

- Generate boxplots, heatmaps, t-SNE, PCA, k-means, and scatter plots.

7) Clustering & Ranking

- Rank based on confidence, clustering, affinity, and similarity to natural Rubisco.



## Installation

**Make sure you have [Conda](https://docs.conda.io/en/latest/miniconda.html) installed first.**

### 1. Clone the repository

git clone https://github.com/emilkack123/BB103X_final.git cd BB103X_final

### 2. Create the main Conda environment

conda env create -f workflow/envs/snakemake_env.yml

### 3. Activate the environment

conda activate snakemake_project

### 4. (Optional) Set up other environments for individual scripts

#### For structure prediction (OmegaFold)
conda env create -f workflow/envs/omegafold.yaml
conda activate omegafold

#### For protein docking
conda env create -f workflow/envs/docking.yml
conda activate vina-docking-env

## Usage, switch the amount of cores to the apprioriate amount

snakemake --cores 4 --use--conda

### Run the full pipeline:

## Authors
Muhammad Ahmad

Moa Cronstrand Elvung

Emil Käck

Sofia Klangby

Supervisor: Ulysse Castet

## License
