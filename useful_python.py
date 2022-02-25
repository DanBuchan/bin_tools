
# use with csv.reader to skip lines that start with a comment character
# reader = csv.reader(skip_comments(scop_list_file,"#"), delimiter=',',
#                     quotechar='"')
def skip_comments(iterable, char):
    for line in iterable:
        if not line.startswith(char):
            yield line

# a nre print statment that sends the contents to stderr
import sys

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
