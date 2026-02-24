import pprint
import re
import sys

"""
    Flattens a fasta file so each sequence is on only a single line. Optionally will send proteins larger than 10k residues to their own file

    # python prep_fasta.py [FILE] 1/0
"""
# print("Usage: >python prepfast.py [FASTA FILE] [1/0]")
header = ""
seq = ""
i = 0

large_ctl = False
if int(sys.argv[2]):
    large_ctl=True

if large_ctl:
    large_seqs = open("10k_sequences.fasta", "w", encoding="utf-8")



with open(sys.argv[1]) as infile:
    for line in infile:
        line = line.strip()
        if line.startswith(">"):
            if i > 0:
                if large_ctl and len(seq) >= 10000:
                    large_seqs.write(f'{header}\n')
                    large_seqs.write(f'{seq}\n')
                else:
                    print(header)
                    print(seq)
            seq = ""
            header = line
            i += 1
        else:
            seq += line

if large_ctl and len(seq) >= 10000:
    large_seqs.write(f'{header}\n')
    large_seqs.write(f'{seq}\n')
else:
    print(header)
    print(seq)


if large_ctl:
    large_seqs.close()

# 22279.out
