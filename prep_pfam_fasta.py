import sys
import random

# a missing one PF06248
# bugged version 9066 families
# grep on "#=GF AC" indicates families 19632

pfam_a_file = sys.argv[1]

fhFasta = open('pfam_fasta.fa', "w")
fhReps = open('reps.fasta.fa', "w")
pfam_family_id = None
current_family = []
family_count = 0
read_count = 0
with open(pfam_a_file, "r", encoding="utf-8", errors="replace") as fh:
    for line in fh:
        # if family_count == 2:
        #     exit()
        if line.startswith("//"):
            if len(current_family) != 0:
                print(f"PRINTING: {pfam_family_id}")
                for line in current_family:
                    entries = line.split()
                    fhFasta.write(f">{entries[0]}|{pfam_family_id}\n")
                    fhFasta.write(f"{entries[1].replace('.','').replace('-','').upper()}\n")
                random_rep = random.choice(current_family)
                entries = random_rep.split()
                fhReps.write(f">{entries[0]}|{pfam_family_id}\n")
                fhReps.write(f"{entries[1].replace('.','').replace('-','').upper()}\n")
                current_family = []
                family_count += 1
                continue
        elif line.startswith("#=GF AC"):
            pfam_family_id = line[10:].split(".")[0]
            read_count += 1
        elif not line.startswith("#"):
            current_family.append(line.rstrip())


if len(current_family) != 0:
    print(f"PRINTING: {pfam_family_id}")
    for line in current_family:
        entries = line.split()
        fhFasta.write(f">{entries[0]}|{pfam_family_id}\n")
        fhFasta.write(f"{entries[1].replace('.','').replace('-','').upper()}\n")
    random_rep = random.choice(current_family)
    entries = random_rep.split()
    fhReps.write(f">{entries[0]}|{pfam_family_id}\n")
    fhReps.write(f"{entries[1].replace('.','').replace('-','').upper()}\n")
    current_family = []
    family_count += 1

fhFasta.close()
fhReps.close()

print(f"FAMILIES READ: {read_count}")
print(f"FAMILIES PRINTED: {family_count}")
