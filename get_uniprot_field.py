import requests
import sys

#
# get_uniprot_field.py ids.txt
#
# Takes a file of IDs (one on each line) and retrieves some
# field from uniprot. So you can do an ID to ID look up.
#
# Currently only support ID to GO terms
#
# Outputs a CSV file of the IDs
#


field = 'GO'
uniprot_uri = 'https://www.uniprot.org/uniprot/'
file = sys.argv[1]
print(file)

id_list = []
with open(file, "r", encoding="utf-8") as fhIn:
    for line in fhIn:
        id_list.append(line.rstrip())



# id_list = ['G3U3H7']
# useful test record
if field == 'GO':
    print('uniprot_id,go_id,evidence')
for up_id in id_list:
    sys.stderr.write(f'GETTING: {uniprot_uri}{up_id}.txt\n')
    r = requests.get(f'{uniprot_uri}{up_id}.txt')
    if r.status_code == 200:
        file_data = r.text.split("\n")
        # Now we can just match:case the field we want
            for entry in file_data:
                if entry.startswith('DR   GO;'):
                    fields = entry[9:].split('; ')
                    print(f'{up_id},{fields[0]},{fields[2]}')
    else:
        sys.stderr.write(f'FAILED: {uniprot_uri}{up_id}.txt\n')
