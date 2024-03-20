import sys

###
# Take a Pfam file in stockholm format and output a fasta version
# python3 prep_pfam_fasta.py ~/Data/pfam/Pfam-A.full.uniprot Pfam-A.full.uniprot.fa

pfam_a_file = sys.argv[1]

fhFasta = open(sys.argv[2], "w")

pfam_family_id = None
current_family = []
family_count = 0
read_count = 0
with open(pfam_a_file, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        # if family_count == 2:
        #     exit()
        if line.startswith("//"):
            if len(current_family) != 0 and pfam_family_id:
                print(f"PRINTING: {pfam_family_id}")
                for line in current_family:
                    entries = line.split()
                    if "/" in entries[1]:
                    ## We should probably tests for all invalid characters and just not output them here
                    ## Might be worth outputting to STDOUT too
                        continue
                    fhFasta.write(f">{entries[0]}|{pfam_family_id}\n")
                    fhFasta.write(f"{entries[1].replace('.','').replace('-','').upper()}\n")
                current_family = []
                pfam_family_id = None
                family_count += 1
                continue
        elif line.startswith("#=GF AC"):
            pfam_family_id = line[10:].split(".")[0]
            read_count += 1
        elif not line.startswith("#"):
            current_family.append(line.rstrip())


if len(current_family) != 0 and pfam_family_id:
    print(f"PRINTING: {pfam_family_id}")
    for line in current_family:
        entries = line.split()
        if "/" in entries[1]:
            continue
        fhFasta.write(f">{entries[0]}|{pfam_family_id}\n")
        fhFasta.write(f"{entries[1].replace('.','').replace('-','').upper()}\n")
    current_family = []
    pfam_family_id = None
    family_count += 1

fhFasta.close()

print(f"FAMILIES READ: {read_count}")
print(f"FAMILIES PRINTED: {family_count}")
