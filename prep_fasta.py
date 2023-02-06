import pprint
import re
import sys

"""
    Flattens a fasta file so each sequence is on only a single line

    # python prep_fasta.py [FILE]
"""
print("Usage: >python prepfast.py [FASTA FILE]")
header = ""
seq = ""
i = 0
with open(sys.argv[1]) as infile:
    for line in infile:
        line = line.strip()
        if line.startswith(">"):
            if i > 0:
                print(header)
                print(seq)
            seq = ""
            header = line
            i += 1
        else:
            seq += line

print(header)
print(seq)

# 22279.out
