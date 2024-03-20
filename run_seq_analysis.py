import argparse
from collections import defaultdict
from subprocess import Popen, PIPE
import sys
from commandRunner.localRunner import *
import os

"""
give it a fasta file and it'll run a blast command over each sequence

python3 run_seq_analysis.py --in_fasta test.fa --blast_command "/home/dbuchan/Applications/ncbi-blast-2.12.0+/bin/psiblast -query \$I1 -db /home/dbuchan/Data/uniref/unitest.fasta -out \$O1" --work_path /home/dbuchan/bin
"""


def write_output(outname, data):
    with open(f'{outname}', "w", encoding="utf-8") as fhOut:
        fhOut.write(f'{data}')


def run_command():
    pass


parser = argparse.ArgumentParser(description='Process a fasta file and run'
                                             ' some tool over it.  Uses '
                                             'commandRunner syntax for the '
                                             'command',
                                 prog='run_seq_analysis.py',
                                 usage='%(prog)s [options] --in_fasta '
                                       '[FILE] --blast_command "'
                                       '"psiblast -query \\$I1 -db '
                                       '~/Data/uniref/unitest.fasta  -out \$O1'
                                       '--work_path /home/thing/test/')
parser.add_argument('--in_fasta', help="A multiple FASTA file that you want to"
                                       " split", required=True)
parser.add_argument('--directory_split',
                    help="Sets whether each file should get its own output "
                         "directory on completion. Or if all the files should"
                         "be left in work_path",
                    action="store_true")
parser.add_argument('--work_path',
                    help="Sets the parent directory for where the work will"
                         "go and be calculated",
                    default="/tmp")
parser.add_argument('--blast_command',
                    help="The command to run, the name of the input file will "
                         "be appended to end so use that to include any input "
                         "flags.",
                    required=True)
args = parser.parse_args()

script_dir = os.getcwd()
fasta_data = {}
name = ''
with open(args.in_fasta, "r", encoding='utf-8') as fhInput:
    for line in fhInput:
        if len(line) <= 1:
            continue
        if line.startswith(">"):
            name = line.split()[0][1:]
            fasta_data[name] = ''
        else:
            fasta_data[name] += line.rstrip()

for name in fasta_data.keys():
    try:
        r = localRunner(tmp_id=name, tmp_path=args.work_path,
                        in_globs=['.fa', ],
                        out_globs=['.bls', ], command=args.blast_command,
                        input_data={f'{name}.fa':
                                    f'>{name}\n{fasta_data[name]}'},
                        std_out_str=f'{name}.stdout')
        r.prepare()
        print(r.command)
        exit_status = r.run_cmd(success_params=[0])
        if exit_status != 0:
            sys.exit(exit_status)
        if args.directory_split:
            print("SPLITTING")
            for file_name in r.output_data.keys():
                write_output(file_name,
                             r.output_data[file_name].decode('utf-8'))
        else:
            print("TIDYING")
            os.chdir(script_dir)
            if os.path.exists(f'{args.work_path}/{name}/{name}.stdout'):
                os.rename(f'{args.work_path}/{name}/{name}.stdout',
                          f'{args.work_path}/{name}.stdout')
            for file_name in r.output_data.keys():
                write_output(file_name,
                             r.output_data[file_name].decode('utf-8'))
            r.tidy()

    except Exception as e:
        print(str(e))
        sys.exit(1)
