import sys
def has_non_english_line(line):
    return any(ord(char) > 127 for char in line)

if __name__ == "__main__":
    SOURCE = sys.stdin if len(sys.argv) < 2 else open(sys.argv[1])
    for line in SOURCE:
        words = line[:-1].split('\t')
        if len(words) < 4:
            continue
        words = [word for word in words
                 if not has_non_english_line(word)]
        if len(words) <= 1:
            continue
        print "\t".join(words)

