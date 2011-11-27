""" TODO DOC STRING """
import sys

def is_not_exist_or_null(array, position):
    return len(array) <= position or array[position] == "NULL"

def clean(source):
    """ TODO DOC STRING """
    for line in source:
        parts = [part for part in line.strip().split('\t') if part != '']
        if len(parts) < 3:
            sys.stderr.write("Skip Error Line: %s\n" % line)
            continue
        if not is_not_exist_or_null(parts, 3) or not is_not_exist_or_null(parts, 4):
            sys.stderr.write("Beyond Ordinary: %s\n" % line)
            continue

        # ADD comments to explain why
        if int(parts[1]) != 0:
            sys.stderr.write("Unacceptable namespace %s(expect 0)\n" % parts[1])
            continue
        key = int(parts[0])
        title = parts[2].replace('_', ' ')
        print "%d\t%s" % (key, title)

if __name__ == "__main__":
    source = sys.stdin
    clean(source)
