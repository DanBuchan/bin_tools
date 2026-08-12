import csv
from collections import defaultdict

def read_pfam_clans_tsv(file):
    """
        take in a pfam clans tsv file from https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/Pfam-A.clans.tsv.gz
        parse this and output a datastructure with all that data
    """
    data_set = []
    with open(file, encoding="utf-8") as fh:

        clanreader = csv.reader(fh, delimiter="\t")
        for entries in clanreader:
            data_set.append({'PFAM_ID': entries[0],
                             'CLAN_ID': entries[1],
                             'CLAN_NAME': entries[2],
                             'DOMAIN_NAME': entries[3],
                             'DESCRIPTION': entries[4],
                             })
    return data_set

    
def get_clan_membership(clan_data):
    """
        take the data from read_pfam_clans_tsv() and return a dict of CLAN_ID to PFAM_ID.
        there is a holding category for IDs in no clan. There is also a 
        hold list for clan vectors if you need it
    """
    clan_membership = defaultdict(list)
    for pfam in clan_data:

        if len(pfam['CLAN_ID']) > 0:
            clan_membership[pfam['CLAN_ID']].append(pfam['PFAM_ID'])
            clan_membership[pfam['CLAN_ID']]['VECTORS']=[]
                                    
        else:
            clan_membership['NO_CLAN'].append(pfam['PFAM_ID'])
    return(clan_membership)


def read_cath_domain_list(file):
    """
        read in a cath domain list from 
        ftp://orengoftp.biochem.ucl.ac.uk/cath/releases/latest-release/cath-classification-data/
        and output the data
    """
    data_set = []
    with open(file, encoding="utf-8") as fh:
        for line in fh:
            entries = line.rstrip().split()
            data_set.append({'DOMAIN_NAME': entries[0],
                             'C': entries[1],
                             'A': entries[2],
                             'T': entries[3],
                             'H': entries[4],
                             'S35': entries[5],
                             'S60': entries[6],
                             'S95': entries[7],
                             'S100': entries[8],  
                             'S100_COUNT': entries[9],
                             'DOMAIN_LENGTH': entries[10],
                             'RESOLUTION': entries[11],                                                        
                             })
    return data_set


def get_group_membership(depth, data):
    """
        takes in a data set read by read_cath_domain_list() and outputs the domains that are members of a 
        heirarchy grouping. Depth assigned where in the heirarchy you wish to measure the groups.
        depth = 1 : C level groups
        depth = 2 : A level groups
        etc...
        max depth is 8 for S100 groups.
    """

    if depth < 1:
        raise Exception("Depth value can not be less than 1 (C level)")
    if depth > 8:
        raise Exception("Depth value can not be greater than 8 (S100 level)")
    group_membership = defaultdict(list)
    for entry in data:
        group_id = ''
        if depth >= 1:
            group_id = f"{entry['C']}."
        if depth >= 2:
            group_id = group_id+f"{entry['A']}."
        if depth >= 3:
            group_id = group_id+f"{entry['T']}."        
        if depth >= 4:
            group_id = group_id+f"{entry['H']}."
        if depth >= 5:
            group_id = group_id+f"{entry['S35']}."
        if depth >= 6:
            group_id = group_id+f"{entry['S60']}."
        if depth >= 7:
            group_id = group_id+f"{entry['S95']}."
        if depth >= 8:
            group_id = group_id+f"{entry['S100']}."
        group_id = group_id.rstrip('.')
        group_membership[group_id].append(entry['DOMAIN_NAME'])

    return group_membership


def read_expasy_ec_membership(file):
    """
        read in an expasy ENZYMES db assignments list of uniprot ID
        https://ftp.expasy.org/databases/enzyme/enzyme.dat
        and output the data.
        This is in Stockholm format but we just write a very basic parser and don't handle all the lines
    """
    data_set = defaultdict(list)
    with open(file, encoding="utf-8") as fh:
        id = ''
        for line in fh:
            entries = line.rstrip().split()
            if entries[0] == 'ID':
               id= entries[1]
            if entries[0] == 'DR':
                fields = line[5:].rstrip().split(";")
                for field in fields:
                    if len(field) > 0:
                        field = field.lstrip().rstrip()
                        data_set[id].append(field)

        return data_set

def change_ec_list_aggregation_depth(depth, dataset):
    """
        take in an EC famiy dataset aggregated at depth 4 and re-aggregate at a different depth
    """
    if depth < 1:
        raise Exception("Depth value can not be less than 1 (Reaction Class level)")
    if depth > 3:
        raise Exception("Depth value can not be greater than 3")
    group_membership = defaultdict(list)
    for code in dataset:
        code_parts = code.split(".")
        family_id = ''
        if depth >= 1:
            family_id = family_id+f"{code_parts[0]}."
        if depth >= 2:
            family_id = family_id+f"{code_parts[1]}."
        if depth >= 3:
            family_id = family_id+f"{code_parts[2]}."
        family_id = family_id.rstrip('.')
        for protein in dataset[code]:
            group_membership[family_id].append(protein)

    return group_membership