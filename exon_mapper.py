#!/usr/bin/env python3

import os, argparse, subprocess
import numpy as np
import pandas as pd
from Bio import SeqIO

parser = argparse.ArgumentParser()
parser.add_argument("--outdir", default="alignments_exon")
args = parser.parse_args()
outdir = args.outdir

# set directory variables, start at the global working directory
gwd = os.getcwd()
hybpiperdirectory = str(gwd+"/steps/hybpiper")

# import recovery statistics
df = pd.read_csv(hybpiperdirectory+"/output/seq_lengths.txt", sep="\t")
df = df.drop(0)

#change directory to ./steps/MAFFT/alignedseq
os.chdir(gwd+"/steps/MAFFT/alignedseq")

# for each aligned locus, identify the two samples with the highest recovery stats
for fn in os.listdir(): #list file in current directory
	locus = fn.split("_")[0] #split file name and select the first as locus
	#locus = fn.split("_")[1]
	if locus in df.columns:
		df_red = df[['Species',locus]].sort_values(locus, ascending=False)
		df_red = df_red.reset_index()
		# first sample
		sp = df_red["Species"][0]
		exon1 = list(SeqIO.parse(hybpiperdirectory+"/"+sp+"/"+locus+"/"+sp+"/sequences/FNA/"+locus+".FNA", "fasta"))[0]
		exon1.id = "exon1"
		# second sample
		sp = df_red["Species"][1]
		exon2 = list(SeqIO.parse(hybpiperdirectory+"/"+sp+"/"+locus+"/"+sp+"/sequences/FNA/"+locus+".FNA", "fasta"))[0]
		exon2.id = "exon2"
		with open("temp.fasta", "w") as output_handle:
			SeqIO.write([exon1, exon2], output_handle, "fasta")
		subprocess.call("mafft --add temp.fasta "+fn+" > ../"+outdir+"/"+fn ,shell=True)
		subprocess.call("rm temp.fasta", shell=True)
	else:
		print(locus+" not there!!!!")
