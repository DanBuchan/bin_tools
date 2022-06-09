import sys
import csv

"""
python3 prep_cath_fasta.py cath-domain-seqs-S95.fa cath-domain-list-S95.txt

take the cath fasta and the domain list and annotate the fasta with the
h-family membership
"""

cath_fasta = sys.argv[1]
cath_domains = sys.argv[2]

print(cath_fasta, cath_domains)

membership = {}
with open(cath_domains) as fh:
    for line in fh:
        line = line.rstrip()
        entries = line.split()
        h_family = f'{entries[1]}.{entries[2]}.{entries[3]}.{entries[4]}'
        membership[entries[0]] = h_family

with open(cath_fasta) as fh:
    for line in fh:
        line = line.rstrip()
        if line.startswith(">"):
            entries = line.split("|")
            bits = entries[2].split("/")
            if bits[0] in membership.keys():
                print(f'{line}|{membership[bits[0]]}')
            else:
                print(line)
        else:
            print(line)
