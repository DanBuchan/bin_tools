import sys

###
### python retrieve_pfam_record.py Pfam-A.full.uniprot PF10417
###

pf_data = sys.argv[1]
pf_id = sys.argv[2]

get_record = False
de = None
record = ''
with open(pf_data, "r", encoding="utf-8", errors="replace") as fhIn:
    for line in fhIn:
        record += line
        if line.startswith("#=GF AC"):
            if pf_id in line:
                get_record = True
            else:
                get_record = False
        if line.startswith("//") and get_record:
            print(record)
            exit()
        if line.startswith("//") and not get_record:
            record = ''
        # print(line)