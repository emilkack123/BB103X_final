

##############################
# 📌 SECTION 1: INPUT FILES
##############################
NAT_FA = "resources/nat.fa"
GEN_FA = "resources/gen.fa"

##############################
# 📌 SECTION 2: RULES
##############################

# ✅ RULE: Clean Natural Sequences
rule clean_natural_fasta:
    input: NAT_FA
    output: "results/nat_cleaned.fa"
    script: "scripts/clean_fasta.py"

# ✅ RULE: Clean Generated Sequences
rule clean_generated_fasta:
    input: GEN_FA
    output: "results/gen_cleaned.fa"
    script: "scripts/clean_fasta.py"
