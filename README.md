# Maesa_sptree
all scripts using in building a species tree of Maesa (Primulaceae s.l.)
Pirada Sumanon, April 2021

## 0. Working directories
The analyses were performed mainly on GenomeDK cluster.
All programs/softwares used in the pipeline that cannot be installed by conda need to be installed at root (`~`)
All data are stored in a project folder `/faststorage/project/Maesa`
- data: directory for raw data with renamed files and also alignments after manual edited (this directory is backed up)
    - `raw`
    - `edited_alignments`
- scripts: all scripts used (this directory is backed up)
- steps: input and output in each step of the pipeline
    - `input_rawreads`: raw reads copied from `../data`
    - `fastqc`: contains 2 subdirectories for the results for raw reads (`fastqc_raw`) and trimmed reads (`fastqc_trimmed`) (NOTE: I run fastqc on Linospadix & my own computer, so this directory is not exist on GenomeDK.)
    - `trimmed`: trimmed reads
    - `hybpiper`: all about hybpiper 
        *Target file needs to be at `~/target`
    - `coverage`: output of coverage trimming 
    - `seq_sets2`: sequence sets after coverage trimming and length filtering
    - `MAFFT`: all related to sequence alignments
    - `optrimal_prepare`


## 1. Quality Control and Read Trimming
Start at the Global Working Directory (main directory with subproject and scripts; in my case, it's `/faststorage/project/Maesa`)
Execute `QC_and_Trim.sh` for running fastqc on raw reads, trimming raw reads with trimmomatic and running fastqc on trimmed reads
- fastqc outputs stored in `fastqc`, inspect the .html outputs for read quality of each sample
- trimmomatic outputs (trimmed reads) stored in `trimmed`

## 2. HybPiper

### 2.1 Mapping reads to genes
by executing `readsfirst.sh` from Global Working Directory (`/faststorage/project/Maesa`, in my case)
### 2.2 Getting statistical summary 
run from within `hybpiper` directory by executing `statsum.sh` 
        this script uses get_seq_lengths.py and test_stats.py of HybPiper and will produce 2 output files
        - seq_lengths.txt for producing a heatmanp in R 
        - stats.txt for summary
### 2.3 Retrieving sequences for exons, introns and supercontigs 
by running `retrieve_seq.sh` from within `hybpiper` directory,
        For intronerate.py, I used intronerate_dev.py instead of the one from release version. (https://github.com/mossmatters/HybPiper/issues/41).
### 2.4 Extracting paralogs
Run `paralog_inv.sh`, then create paralog_genelist.txt and execute `paralog_retrieve.sh`

>To create a paralog genelist, use the file obtained from previous step/copy the output printed on screen while running `paralog_inv.sh`, remove all the information from it except for the gene name. 
>Example: '2 paralogs written for Gene001' changes to 'Gene001'. Then delete any duplicated lines. In some text editor, go to "Text->Process Duplicated Lines". One gene per line.

For more detail on paralogs: https://github.com/mossmatters/HybPiper/wiki/Paralogs


## 3. Coverage trimming and length filtering
*This part followed Wolf Eiserhardt's scripts for Dypsidinae_species_tree*
In a global working directory (`/faststorage/project/Maesa`, in my case), run `coverage_use.sh`
This script will execute `coverage.py` then `samples2genes.py`.
Output: the new gene fasta files with coverage trimming will be saved in `seq_sets2` and ready for alignment.

## 4. Alignment
### 4.1 Sequence alignment using MAFFT
From GWD, run `MAFFT.sh`.
The aligned sequences will be stored in `MAFFT/alignedseq`.

### 4.2 Mapping exons to alignments
This step creates new alignments that contain the original alignments plus the exon sequences of the two species that had the highest recovery success at each locus. Using `exon_mapper.py` written by Wolf Eiserhardt.
The outputs will be stored in `MAFFT/aligned_exon`.

## 5. Gap trimming
### 5.1 preparation
- prepare alignments by executing `optrimal_prepare.sh`
- generate `cutoff_trim.txt` with desired `-gt` values to be tested (one value per line). For example:
```
0
0.2
0.3
0.4
0.5
0.6
0.7
1
```
### 5.2 optrimAL











[q1=[\w+]+;q2=[\w+]+;q3=[\w+]+;f1=[\d,.,E,-]+;f2=[\d,.,E,-]+;f3=[\d,.,E,-]+;pp1=[\d,.,E,-]+;pp2=[\d,.,E,-]+;pp3=[\d,.,E,-]+;QC=[\d,.,E,-]+;EN=([\d,.,E,-]+)]

