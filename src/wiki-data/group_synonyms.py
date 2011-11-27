import sys

def group(source):
    groups = {}
    for line in source:
        parts = line.strip().split('\t')
        groups.setdefault(parts[2], [parts[2]]).append(parts[1])
    return groups

def print_groups(groups):
    for key, synonyms in groups.items():
        print "\t".join(synonyms)

if __name__ == "__main__":
    SOURCE = sys.stdin if len(sys.argv) < 2 else open(sys.argv[1])
    GROUPS = group(SOURCE)
    print_groups(GROUPS)



