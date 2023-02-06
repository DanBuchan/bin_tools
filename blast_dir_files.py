import pprint
import sys
import os
import subprocess
from multiprocessing import Pool
import glob

"""
   Takes a dir containing fasta files and runs blast on each one.
   Also takes an output directory

   # python blast_dir_files.py
"""
print("Usage: >python blast_dir_files.py [DIR]")
def run_blast(file):
    fasta_id = file.strip(".fasta")
    exe = "/scratch0/NOT_BACKED_UP/dbuchan/Applications/ncbi-blast-2.2.31+/bin/psiblast"
    db = "/scratch0/NOT_BACKED_UP/dbuchan/uniref/test_db.fasta"
    print(fasta_id)
    args = [exe,
            "-query", file,
            "-db",  db,
            "-inclusion_ethresh", "0.001",
            "-out_pssm", fasta_id+".chk",
            "-out", fasta_id+".bls",
            "-num_iterations", "3",
            "-num_alignments", "0",
            "-num_threads", "5"]
    code = subprocess.call(' '.join(args), shell=True)
    print(fasta_id+" exit status: "+str(code))


fasta_dir = "/cs/research/bioinf/home1/green/dbuchan/fasta_test/"
# fasta= open("pdb_2015.fasta", "w")
p = Pool(4)
p.map(run_blast, glob.glob(fasta_dir+"*.fasta"))
