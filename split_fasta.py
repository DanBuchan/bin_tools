import pprint
import re
import sys

"""
   File takes a fasta files and a path and outputs each sequence in it's
   own file

   # python split_fasta.py [FILE] [PATH]
"""
print("Usage: > python split_fasta.py [FASTA FILE] [PATH]")
header = ""
seq = ""
uniref_id = ""
# pattern = re.compile("^>.+?\|(.+?)\|.+?\s")
pattern = re.compile("^>(.+?)\s+")
with open(sys.argv[1]) as infile:
    for line in infile:
        # line = line.strip()
        if line.startswith(">"):
            if len(uniref_id) is not 0:
                out = open(sys.argv[2]+"/"+uniref_id+".fasta", "w")
                out.write(header)
                out.write(seq)
                out.close()
            seq = ""
            header = ""
            header = line
            m = pattern.match(line)
            uniref_id = m.group(1)
        else:
            seq += line
