import sys

count = 0
with open(sys.argv[1], "r") as fh:
    for line in fh:
        if line.startswith(">"):
            count+=1
            line = line.rstrip()
            print(f'>{count}|{line[1:]}')
        else:
            line = line.rstrip()
            print(line)
